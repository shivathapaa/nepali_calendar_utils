"""Predicate over a date that consumers use to enable or disable individual days
and years.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.NepaliSelectableDates``. The UI in
the Kotlin library consults this; in Python it is useful for validating whether a
date is allowed by some rule (range, weekend, holiday, ...). The converter
factories (``NepaliDateConverter.before_date_selectable`` etc.) and the holiday
helpers produce instances of this type.
"""


class NepaliSelectableDates:
    """Base predicate. Both methods default to allowing everything.

    Subclass and override, or use the converter/holiday factories which return
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

    Internal helper used by the converter factories and holiday wrappers so they
    do not each need a bespoke subclass. A ``None`` predicate defaults to ``True``.
    """

    def __init__(self, date_predicate=None, year_predicate=None):
        self._date_predicate = date_predicate
        self._year_predicate = year_predicate

    def is_selectable_date(self, custom_calendar) -> bool:
        return self._date_predicate(custom_calendar) if self._date_predicate else True

    def is_selectable_year(self, year: int) -> bool:
        return self._year_predicate(year) if self._year_predicate else True
