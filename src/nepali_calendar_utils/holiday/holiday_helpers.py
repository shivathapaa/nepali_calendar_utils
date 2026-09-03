"""Selectable-date wrappers and working-day arithmetic over a holiday provider.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.holiday.HolidayHelpers``. In Kotlin
these are extension functions on ``NepaliDateConverter``; here they are module
functions (also surfaced as static methods on ``NepaliDateConverter`` for
convenience).
"""

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.nepali_selectable_dates import (
    NepaliSelectableDates,
    _FunctionalSelectableDates,
)
from nepali_calendar_utils.holiday.holiday_provider import NepaliHolidayProvider, NepaliWeekend


# NepaliSelectableDates wrappers

def excluding_holidays(base: NepaliSelectableDates, provider: NepaliHolidayProvider) -> NepaliSelectableDates:
    """Wrap ``base`` so it additionally rejects any date flagged by ``provider``.

    Year-level selection still defers to ``base`` - holiday data is per-date, not
    per-year.
    """
    def date_predicate(cc):
        return base.is_selectable_date(cc) and not provider.is_holiday(
            SimpleDate(cc.year, cc.month, cc.day_of_month)
        )
    return _FunctionalSelectableDates(date_predicate=date_predicate, year_predicate=base.is_selectable_year)


def excluding_weekends(base: NepaliSelectableDates, weekend=NepaliWeekend.Default) -> NepaliSelectableDates:
    """Wrap ``base`` so it additionally rejects weekend days.

    ``weekend`` is a set of 1-based-Sunday day-of-week numbers (Sunday = 1, ...,
    Saturday = 7). Defaults to Saturday only.
    """
    def date_predicate(cc):
        return base.is_selectable_date(cc) and cc.day_of_week not in weekend
    return _FunctionalSelectableDates(date_predicate=date_predicate, year_predicate=base.is_selectable_year)


# Working-day arithmetic

def working_days_between(start: SimpleDate, end: SimpleDate, provider: NepaliHolidayProvider,
                         weekend=NepaliWeekend.Default) -> int:
    """Number of working days in the half-open range ``[start, end)``.

    Skips both ``weekend`` days and dates flagged by ``provider``. ``end`` is
    exclusive (matches ``get_nepali_days_in_between``). Requires ``start <= end``;
    returns 0 when ``start == end``.

    Raises:
        ValueError: if ``start > end``.
    """
    from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
    if start > end:
        raise ValueError(f"start ({start}) must be <= end ({end})")
    span = NepaliDateConverter.get_nepali_days_in_between(start, end)
    if span <= 0:
        return 0

    count = 0
    for offset in range(span):
        cal = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            start.year, start.month, start.day_of_month, offset
        )
        if cal.day_of_week in weekend:
            continue
        if provider.is_holiday(SimpleDate(cal.year, cal.month, cal.day_of_month)):
            continue
        count += 1
    return count


def next_working_day(from_date: SimpleDate, provider: NepaliHolidayProvider,
                     weekend=NepaliWeekend.Default) -> SimpleDate:
    """First working day at or after ``from_date``.

    If ``from_date`` is itself a working day, returns it unchanged. Bounded scan -
    gives up after a year.

    Raises:
        RuntimeError: if no working day is found within 366 days.
    """
    from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
    offset = 0
    while offset <= 366:
        cal = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            from_date.year, from_date.month, from_date.day_of_month, offset
        )
        simple = SimpleDate(cal.year, cal.month, cal.day_of_month)
        if cal.day_of_week not in weekend and not provider.is_holiday(simple):
            return simple
        offset += 1
    raise RuntimeError(
        f"next_working_day: no working day found within 366 days of {from_date} - "
        "check your NepaliHolidayProvider and weekend set"
    )


def add_working_days(from_date: SimpleDate, days: int, provider: NepaliHolidayProvider,
                     weekend=NepaliWeekend.Default) -> SimpleDate:
    """Date that is ``days`` working days from ``from_date`` (Excel ``WORKDAY`` semantics).

    - ``days == 0`` returns ``from_date`` unchanged.
    - ``days > 0`` returns the ``days``-th working day strictly after ``from_date``.
    - ``days < 0`` returns the ``abs(days)``-th working day strictly before it.

    Note this means ``add_working_days(from_date, 0)`` is not the same as
    ``next_working_day(from_date)`` - use the latter for adjustment.

    Raises:
        RuntimeError: if more than ~2 years of scanning fails (guards against
        pathological providers).
    """
    from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
    if days == 0:
        return from_date
    step = 1 if days > 0 else -1
    remaining = abs(days)
    offset = 0
    max_scan = 732  # ~2 years of slack

    while remaining > 0:
        offset += step
        if offset > max_scan or offset < -max_scan:
            raise RuntimeError(
                f"add_working_days: exceeded {max_scan}-day scan from {from_date} "
                f"when looking for {days} working days"
            )
        cal = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            from_date.year, from_date.month, from_date.day_of_month, offset
        )
        if cal.day_of_week in weekend:
            continue
        if provider.is_holiday(SimpleDate(cal.year, cal.month, cal.day_of_month)):
            continue
        remaining -= 1

    final = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
        from_date.year, from_date.month, from_date.day_of_month, offset
    )
    return SimpleDate(final.year, final.month, final.day_of_month)
