"""The two calendar systems this library speaks.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.data.CalendarSystem``.
"""

from enum import Enum
from typing import Optional


class CalendarSystem(Enum):
    """A calendar system, identified by the ``era`` a :class:`CustomCalendar` carries.

    This is the named form of the ``era`` integer on :class:`CustomCalendar` and
    :class:`MonthCalendar` (1 = AD, 2 = BS), so the two representations never disagree:
    :attr:`era` is the single mapping.

    A calendar carries the system it was read in, so
    ``NepaliDateConverter.get_english_calendar(...)`` answers :attr:`GREGORIAN` and
    ``get_nepali_calendar(...)`` answers :attr:`BIKRAM_SAMBAT`.
    """

    #: Bikram Sambat, the official calendar of Nepal. ``era`` 2.
    BIKRAM_SAMBAT = 2

    #: Gregorian, referred to as the English or AD calendar throughout this library. ``era`` 1.
    GREGORIAN = 1

    @property
    def era(self) -> int:
        """The ``era`` value a ``CustomCalendar`` in this system carries."""
        return self.value

    def opposite(self) -> "CalendarSystem":
        """The other system. With two systems this is the toggle target."""
        return CalendarSystem.GREGORIAN if self is CalendarSystem.BIKRAM_SAMBAT else CalendarSystem.BIKRAM_SAMBAT

    @classmethod
    def from_era(cls, era: int) -> Optional["CalendarSystem"]:
        """The system carrying ``era``, or ``None`` when ``era`` is neither 1 nor 2.

        Returns ``None`` rather than raising because ``era`` reaches this from parsed and
        restored values that callers are expected to fall back on, not to crash over.
        """
        for system in cls:
            if system.value == era:
                return system
        return None
