"""The holiday provider SPI under its former names.

A holiday turned out to be one kind of event rather than the whole subject: the
package also names festivals, school programmes, deadlines and birthdays, and
whether a day is worked is now ``NepaliCalendarEvent.closes_offices`` rather than
something the taxonomy decides. Everything here still works and resolves to the
types in :mod:`nepali_calendar_utils.event`.
"""

from typing import Set

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.event.nepali_calendar_event import (
    NepaliCalendarEvent,
    NepaliEventKind,
)
from nepali_calendar_utils.event.nepali_event_provider import (
    NepaliEventProvider,
    NepaliWeekend,
)

#: Former name of :class:`~nepali_calendar_utils.event.NepaliEventKind`. The members
#: and their values are unchanged.
HolidayKind = NepaliEventKind

#: Former name of :class:`~nepali_calendar_utils.event.NepaliCalendarEvent`, which
#: takes the same three positional arguments and adds ``closes_offices``, ``id`` and
#: ``payload``.
HolidayEntry = NepaliCalendarEvent


class NepaliHolidayProvider(NepaliEventProvider):
    """Former name of :class:`~nepali_calendar_utils.event.NepaliEventProvider`, kept
    as a class of its own so an implementation written against it keeps working.

    Subclasses implement :meth:`holidays` and optionally :meth:`is_holiday`, and the
    policy, the picker wrappers and the working-day helpers reach them through
    ``events`` and ``closes_on``. A subclass keeps the older, blunter rule that every
    entry closes the day: ``closes_offices`` is not consulted, so an observance
    returned from :meth:`holidays` still blocks its date and still stops a working-day
    count. Implement :class:`~nepali_calendar_utils.event.NepaliEventProvider`
    directly for the finer answer.
    """

    def holidays(self, year: int) -> Set[NepaliCalendarEvent]:
        """All holidays for ``year`` (BS). An empty set is a valid answer."""
        raise NotImplementedError

    def is_holiday(self, date: SimpleDate) -> bool:
        """``True`` if any entry from :meth:`holidays` for ``date.year`` falls on ``date``.

        Default implementation re-queries :meth:`holidays` on every call. Override
        with a memoized implementation if you call this in tight loops.
        """
        return any(entry.date == date for entry in self.holidays(date.year))

    def events(self, year: int) -> Set[NepaliCalendarEvent]:
        return self.holidays(year)

    def closes_on(self, date: SimpleDate) -> bool:
        return self.is_holiday(date)


class _NoOpHolidayProvider(NepaliHolidayProvider):
    """Behaves as if no day is a holiday."""

    def holidays(self, year: int) -> Set[NepaliCalendarEvent]:
        return set()

    def is_holiday(self, date: SimpleDate) -> bool:
        return False


#: Former name of :data:`~nepali_calendar_utils.event.NoOpEventProvider`, answering
#: to ``holidays`` and ``is_holiday`` as well.
NoOpHolidayProvider = _NoOpHolidayProvider()

__all__ = [
    "HolidayKind",
    "HolidayEntry",
    "NepaliHolidayProvider",
    "NoOpHolidayProvider",
    "NepaliWeekend",
]
