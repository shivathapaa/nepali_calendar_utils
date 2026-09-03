"""Service-provider interface for supplying Nepali holiday data.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.holiday.NepaliHolidayProvider`` and
friends.

This library ships **no holiday data** by design - Nepali public, religious, and
regional holiday lists change year to year, and baking stale data into the library
would not serve consumers. Implement :class:`NepaliHolidayProvider` with your own
source (a static map, a CMS, an HR API, ...) and pass it to the helpers in
:mod:`nepali_calendar_utils.holiday.holiday_helpers`.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Set

from nepali_calendar_utils.data.custom_calendar import SimpleDate


class HolidayKind(Enum):
    """Categorization for a :class:`HolidayEntry`.

    Deliberately narrow - adding cases is a breaking change. If your taxonomy
    needs more granularity, store extra fields on a wrapper type.
    """

    #: Bank / government office is closed. Sarkari bida.
    GOVERNMENT_PUBLIC = "government_public"

    #: Religious or cultural holiday - Dashain, Tihar, Holi, Id, Christmas, etc.
    RELIGIOUS = "religious"

    #: Province- or district-level holiday, not nationally observed.
    REGIONAL = "regional"

    #: Recognized day but offices remain open (e.g. World Health Day).
    OBSERVANCE = "observance"


@dataclass(frozen=True)
class HolidayEntry:
    """A single holiday in the Nepali (Bikram Sambat) calendar.

    Attributes:
        date (SimpleDate): Bikram Sambat date of the holiday.
        name (str): Display name (e.g. "Dashain - Vijaya Dashami").
        kind (HolidayKind): Category - see :class:`HolidayKind`.
    """

    date: SimpleDate
    name: str
    kind: HolidayKind


class NepaliHolidayProvider:
    """Interface for supplying holiday data.

    Implementations must:
      - return a stable set for a given ``year`` (calling twice yields the same
        contents),
      - not raise for years outside the supported Nepali year range - return an
        empty set instead.

    Example::

        class MyHolidays(NepaliHolidayProvider):
            _by_year = {
                2082: {
                    HolidayEntry(SimpleDate(2082, 1, 1), "नयाँ वर्ष",
                                 HolidayKind.GOVERNMENT_PUBLIC),
                },
            }
            def holidays(self, year):
                return self._by_year.get(year, set())
    """

    def holidays(self, year: int) -> Set[HolidayEntry]:
        """All holidays for ``year`` (BS). An empty set is a valid answer."""
        raise NotImplementedError

    def is_holiday(self, date: SimpleDate) -> bool:
        """``True`` if any entry from :meth:`holidays` for ``date.year`` falls on ``date``.

        Default implementation re-queries :meth:`holidays` on every call. Override
        with a memoized implementation if you call this in tight loops.
        """
        return any(entry.date == date for entry in self.holidays(date.year))


class _NoOpHolidayProvider(NepaliHolidayProvider):
    """Behaves as if no day is a holiday."""

    def holidays(self, year: int) -> Set[HolidayEntry]:
        return set()

    def is_holiday(self, date: SimpleDate) -> bool:
        return False


#: No-op provider singleton. Use when you want the holiday-aware APIs but have not
#: (yet) wired a real data source.
NoOpHolidayProvider = _NoOpHolidayProvider()


class NepaliWeekend:
    """Day-of-week conventions.

    The library uses a 1-based-Sunday convention everywhere - Sunday = 1, ...,
    Saturday = 7.
    """

    #: Default weekend in Nepal: Saturday only. Nepal observes a single-day
    #: weekend, so working-day arithmetic that uses this matches what a Nepali
    #: office counts as "5 working days from today". Pass ``frozenset({6, 7})``
    #: for a Friday-and-Saturday weekend.
    Default = frozenset({7})
