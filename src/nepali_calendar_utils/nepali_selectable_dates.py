"""Predicate over a date that consumers use to enable or disable individual days
and years.

Useful for validating whether a date is allowed by some rule: a range, a weekend, a
day the institution is closed. The converter factories
(``NepaliDateConverter.before_date_selectable`` and the like), the event helpers and
``NepaliCalendarPolicy.as_selectable_dates`` all produce instances of this type.
"""


class NepaliSelectableDates:
    """Base predicate. Both methods default to allowing everything.

    Subclass and override, or use the converter and event factories, which return
    ready-made instances.
    """

    def is_selectable_date(self, custom_calendar) -> bool:
        """Return ``True`` if ``custom_calendar`` should be selectable."""
        return True

    def is_selectable_year(self, year: int) -> bool:
        """Return ``True`` if ``year`` should be selectable.

        When a year is not selectable, all dates in that year are also not
        selectable.
        """
        return True


class _FunctionalSelectableDates(NepaliSelectableDates):
    """A :class:`NepaliSelectableDates` backed by two optional predicates.

    Internal helper used by the converter factories and the event wrappers so they
    do not each need a bespoke subclass. A ``None`` predicate defaults to ``True``.
    """

    def __init__(self, date_predicate=None, year_predicate=None):
        self._date_predicate = date_predicate
        self._year_predicate = year_predicate

    def is_selectable_date(self, custom_calendar) -> bool:
        return self._date_predicate(custom_calendar) if self._date_predicate else True

    def is_selectable_year(self, year: int) -> bool:
        return self._year_predicate(year) if self._year_predicate else True
