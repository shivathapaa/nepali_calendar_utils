"""A month's grid geometry, tagged with the calendar system it is expressed in.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.data.MonthCalendar``.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from nepali_calendar_utils.data.calendar_system import CalendarSystem

if TYPE_CHECKING:
    from nepali_calendar_utils.data.custom_calendar import NepaliMonthCalendar


@dataclass(frozen=True)
class MonthCalendar:
    """One month of either calendar, carrying the system it belongs to.

    :class:`NepaliMonthCalendar` describes a Bikram Sambat month only. This says the same
    things about a month of either calendar, so a caller laying out a grid does not have to
    know which system produced it.

    Attributes:
        calendar_system (CalendarSystem): The system ``year`` and ``month`` are expressed in.
        year (int): The year in ``calendar_system``.
        month (int): The month (1-12). 1 is Baisakh in Bikram Sambat, January in Gregorian.
        total_days_in_month (int): The number of days in the month (28-32, depending on the calendar).
        first_day_of_month (int): The day of the week (1-7, where 1 is Sunday) the month starts on.
        last_day_of_month (int): The day of the week (1-7, where 1 is Sunday) the month ends on.
    """

    calendar_system: CalendarSystem
    year: int
    month: int
    total_days_in_month: int
    first_day_of_month: int
    last_day_of_month: int

    @property
    def days_from_start_of_week_to_first_of_month(self) -> int:
        """Leading blank cells before day 1 when the grid starts on Sunday."""
        return self.first_day_of_month - 1

    def index_in(self, years: range) -> int:
        """The position of this month within ``years``, counting 12 months per year.

        ``years`` must be a range in the same :attr:`calendar_system`.
        """
        return (self.year - years.start) * 12 + self.month - 1

    def to_nepali_month_calendar(self) -> "NepaliMonthCalendar":
        """Narrow this month to the Bikram Sambat-only :class:`NepaliMonthCalendar`.

        The year and month are copied verbatim, so calling this on a
        :attr:`CalendarSystem.GREGORIAN` month produces a ``NepaliMonthCalendar`` holding
        Gregorian numbers. Convert the month to Bikram Sambat first when that matters.
        """
        # Imported here rather than at module scope: custom_calendar imports this module for
        # NepaliMonthCalendar.to_month_calendar, so a top-level import would close the cycle.
        from nepali_calendar_utils.data.custom_calendar import NepaliMonthCalendar

        return NepaliMonthCalendar(
            year=self.year,
            month=self.month,
            total_days_in_month=self.total_days_in_month,
            first_day_of_month=self.first_day_of_month,
            last_day_of_month=self.last_day_of_month,
        )
