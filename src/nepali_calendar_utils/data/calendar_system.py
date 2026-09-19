"""The two calendar systems this library speaks.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.data.CalendarSystem``.
"""

from enum import Enum
from typing import Optional


class CalendarSystem(Enum):
    """A calendar system, identified by the ``era`` a :class:`CustomCalendar` carries.

    A date is always stored as :attr:`BIKRAM_SAMBAT` whichever system it is read in, so
    moving between the two is lossless.
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
