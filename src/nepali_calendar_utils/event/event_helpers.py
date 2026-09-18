"""Selectable-date wrappers and working-day arithmetic over a calendar's events.

The arithmetic helpers are also surfaced as static methods on
``NepaliDateConverter``. Each of them takes either a provider and a weekend set, or a
:class:`~nepali_calendar_utils.event.nepali_calendar_policy.NepaliCalendarPolicy`,
which already states both.
"""

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.nepali_selectable_dates import (
    NepaliSelectableDates,
    _FunctionalSelectableDates,
)
from nepali_calendar_utils.event.nepali_event_provider import NepaliEventProvider, NepaliWeekend

#: A year of scanning, the point at which a forward search gives up rather than
#: looping on a policy that closes every day.
MAX_FORWARD_SCAN_DAYS = 366

#: About two years of slack, the bound on a working-day count in either direction.
MAX_WORKING_DAY_SCAN_DAYS = 732


def excluding_closures(
    base: NepaliSelectableDates, provider: NepaliEventProvider
) -> NepaliSelectableDates:
    """Wrap ``base`` so it additionally rejects any date ``provider`` says the
    institution is shut for.

    An event that does not close, a programme or a meeting, leaves its day
    selectable: the day is still worked, and refusing it would surprise anyone
    booking on it.

    Year-level rejection still defers to the wrapped predicate, since event data is
    per-date.
    """
    def date_predicate(custom_calendar):
        return base.is_selectable_date(custom_calendar) and not provider.closes_on(
            SimpleDate(
                custom_calendar.year, custom_calendar.month, custom_calendar.day_of_month
            )
        )

    return _FunctionalSelectableDates(
        date_predicate=date_predicate, year_predicate=base.is_selectable_year
    )


def excluding_weekends(
    base: NepaliSelectableDates, weekend=NepaliWeekend.Default
) -> NepaliSelectableDates:
    """Wrap ``base`` so it additionally rejects weekend days.

    ``weekend`` is a set of 1-based-Sunday day-of-week numbers (Sunday = 1, ...,
    Saturday = 7). Defaults to Saturday only. Pass ``frozenset({6, 7})`` for a
    Friday-and-Saturday weekend.
    """
    def date_predicate(custom_calendar):
        return (
            base.is_selectable_date(custom_calendar)
            and custom_calendar.day_of_week not in weekend
        )

    return _FunctionalSelectableDates(
        date_predicate=date_predicate, year_predicate=base.is_selectable_year
    )


def working_days_between(start: SimpleDate, end: SimpleDate, provider, weekend=None) -> int:
    """Number of working days in the half-open range ``[start, end)``.

    Skips both the weekend days and the dates the institution is shut for. ``end`` is
    exclusive, matching ``get_nepali_days_in_between``; to make it inclusive, add 1
    when ``end`` itself is a working day. A day that is both a weekend and a closure
    is skipped once. Returns 0 when ``start == end``.

    Args:
        start (SimpleDate): First day of the range, included.
        end (SimpleDate): Day the range stops before.
        provider: A :class:`NepaliEventProvider`, or a ``NepaliCalendarPolicy`` that
            carries its own weekly off days.
        weekend: Day-of-week numbers treated as the weekend. Defaults to Saturday
            only, and must be left unset when a policy is passed.

    Raises:
        ValueError: if ``start > end``, or if both a policy and a ``weekend`` are given.
    """
    from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

    provider, weekend = _resolve_provider_and_weekend(provider, weekend)
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
        if provider.closes_on(SimpleDate(cal.year, cal.month, cal.day_of_month)):
            continue
        count += 1
    return count


def next_working_day(from_date: SimpleDate, provider, weekend=None) -> SimpleDate:
    """First working day at or after ``from_date``.

    If ``from_date`` is itself a working day, returns it unchanged. Otherwise scans
    forward day by day, bounded: gives up after a year rather than looping forever on
    a policy that closes every day.

    Args:
        from_date (SimpleDate): Day to start looking from, included.
        provider: A :class:`NepaliEventProvider`, or a ``NepaliCalendarPolicy`` that
            carries its own weekly off days.
        weekend: Day-of-week numbers treated as the weekend. Defaults to Saturday
            only, and must be left unset when a policy is passed.

    Raises:
        ValueError: if both a policy and a ``weekend`` are given.
        RuntimeError: if no working day is found within 366 days.
    """
    from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

    provider, weekend = _resolve_provider_and_weekend(provider, weekend)
    offset = 0
    while offset <= MAX_FORWARD_SCAN_DAYS:
        cal = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            from_date.year, from_date.month, from_date.day_of_month, offset
        )
        simple = SimpleDate(cal.year, cal.month, cal.day_of_month)
        if cal.day_of_week not in weekend and not provider.closes_on(simple):
            return simple
        offset += 1
    raise RuntimeError(
        f"next_working_day: no working day found within {MAX_FORWARD_SCAN_DAYS} days of "
        f"{from_date} - check your NepaliEventProvider and weekend set"
    )


def add_working_days(from_date: SimpleDate, days: int, provider, weekend=None) -> SimpleDate:
    """Date that is ``days`` working days from ``from_date`` (Excel ``WORKDAY`` semantics).

    - ``days == 0`` returns ``from_date`` unchanged.
    - ``days > 0`` returns the ``days``-th working day strictly after ``from_date``.
    - ``days < 0`` returns the ``abs(days)``-th working day strictly before it.

    Note this means ``add_working_days(from_date, 0)`` is not the same as
    :func:`next_working_day` - use the latter for adjustment.

    Args:
        from_date (SimpleDate): Day the count starts from, itself never the answer
            unless ``days`` is 0.
        days (int): How many working days to move, forward when positive.
        provider: A :class:`NepaliEventProvider`, or a ``NepaliCalendarPolicy`` that
            carries its own weekly off days.
        weekend: Day-of-week numbers treated as the weekend. Defaults to Saturday
            only, and must be left unset when a policy is passed.

    Raises:
        ValueError: if both a policy and a ``weekend`` are given.
        RuntimeError: if more than about two years of scanning fails, which guards
            against a policy that closes every day.
    """
    from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

    provider, weekend = _resolve_provider_and_weekend(provider, weekend)
    if days == 0:
        return from_date
    step = 1 if days > 0 else -1
    remaining = abs(days)
    offset = 0

    while remaining > 0:
        offset += step
        if abs(offset) > MAX_WORKING_DAY_SCAN_DAYS:
            raise RuntimeError(
                f"add_working_days: exceeded {MAX_WORKING_DAY_SCAN_DAYS}-day scan from "
                f"{from_date} when looking for {days} working days"
            )
        cal = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            from_date.year, from_date.month, from_date.day_of_month, offset
        )
        if cal.day_of_week in weekend:
            continue
        if provider.closes_on(SimpleDate(cal.year, cal.month, cal.day_of_month)):
            continue
        remaining -= 1

    final = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
        from_date.year, from_date.month, from_date.day_of_month, offset
    )
    return SimpleDate(final.year, final.month, final.day_of_month)


def _resolve_provider_and_weekend(provider, weekend):
    """Split a policy into the provider and weekend the arithmetic works in terms of,
    or pass a plain provider through with the default weekend."""
    # Imported here rather than at module scope because the policy composes these helpers.
    from nepali_calendar_utils.event.nepali_calendar_policy import NepaliCalendarPolicy

    if isinstance(provider, NepaliCalendarPolicy):
        if weekend is not None:
            raise ValueError(
                "weekend is already part of the policy: pass a policy or a provider and a "
                "weekend, not both"
            )
        return provider.provider, provider.weekly_off_days
    return provider, NepaliWeekend.Default if weekend is None else weekend
