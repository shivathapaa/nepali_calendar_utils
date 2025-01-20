from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class SimpleDate:
    """
    Represents a simple date with year, month, and day of the month.
    """
    year: int
    month: int
    day_of_month: int = 1

    def index_in(self, years: range) -> int:
        """
        Returns the position of a SimpleDate within a given years range.
        """
        return (self.year - years.start) * 12 + self.month - 1


@dataclass(frozen=True)
class SimpleTime:
    """
    Represents a 24Hrs format time of day (hour, minute, second, nanosecond).
    Strictly adjusted to the `Asia/Kathmandu` TimeZone.
    """
    hour: int
    minute: int
    second: int
    nanosecond: int

@dataclass(frozen=True)
class NepaliMonthCalendar:
    """
    Represents a calendar month in the Nepali calendar system.
    """
    year: int
    month: int
    total_days_in_month: int
    first_day_of_month: int
    last_day_of_month: int
    days_from_start_of_week_to_first_of_month: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'days_from_start_of_week_to_first_of_month', self.first_day_of_month - 1)
        
    def index_in(self, years: range) -> int:
        """
        Returns the position of a NepaliMonthCalendar within a given years range.
        """
        return (self.year - years.start) * 12 + self.month - 1


@dataclass(frozen=True)
class CustomCalendar:
    """
    Represents a date in a custom calendar system with detailed information.
    """
    year: int
    month: int
    day_of_month: int
    era: int  # 1 for AD, 2 for BS
    first_day_of_month: int
    last_day_of_month: int
    total_days_in_month: int
    day_of_week_in_month: int = -1
    day_of_week: int = -1
    day_of_year: int = -1
    week_of_month: int = -1
    week_of_year: int = -1

    def to_simple_date(self) -> SimpleDate:
        """
        Converts this CustomCalendar object to a SimpleDate object.
        """
        return SimpleDate(
            year=self.year, month=self.month, day_of_month=self.day_of_month
        )

    def to_nepali_month_calendar(self) -> NepaliMonthCalendar:
        """
        Converts this CustomCalendar object to a NepaliMonthCalendar object.
        """
        return NepaliMonthCalendar(
            year=self.year,
            month=self.month,
            total_days_in_month=self.total_days_in_month,
            first_day_of_month=self.first_day_of_month,
            last_day_of_month=self.last_day_of_month,
            # days_from_start_of_week_to_first_of_month=self.first_day_of_month - 1,
        )