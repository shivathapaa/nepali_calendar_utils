from dataclasses import dataclass, field

@dataclass(frozen=True)
class SimpleDate:
    """
    Represents a simple date with year, month, and day of the month.

    Attributes:
        year (int): The year.
        month (int): The month (1-12).
        day_of_month (int): The day of the month (1-32). Defaults to 1.
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
    Represents a 24-hour format time of day (hour, minute, second, nanosecond).
    Strictly adjusted to the `Asia/Kathmandu` time zone.

    Attributes:
        hour (int): Hour of the day (0-23).
        minute (int): Minute of the hour (0-59).
        second (int): Second of the minute (0-59).
        nanosecond (int): Nanosecond of the second (0-999,999,999).
    """
    
    hour: int
    minute: int
    second: int
    nanosecond: int

@dataclass(frozen=True)
class NepaliMonthCalendar:
    """
    Represents a calendar month in the Nepali calendar system.

    This data class provides information about a specific month in a Nepali calendar year,
    including the total number of days, the day of the week for the first and last days of the month,
    and the number of days from the start of the week to the first day of the month.

    Attributes:
        year (int): The Nepali year.
        month (int): The Nepali month (1-12).
        total_days_in_month (int): The total number of days in the month (1-32).
        first_day_of_month (int): The day of the week (1-7, where 1 is Sunday) for the first day of the month.
        last_day_of_month (int): The day of the week (1-7, where 1 is Sunday) for the last day of the month.
        days_from_start_of_week_to_first_of_month (int): The number of days from the start of the week 
            (Sunday) to the first day of the month.
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

    This data class holds information about a specific date, including its year, month, day,
    era (AD or BS), and various other properties related to the day and week within the month and year.

    Attributes:
        year (int): The year in the custom calendar.
        month (int): The month in the custom calendar (1-12).
        day_of_month (int): The day of the month (1-32).
        era (int): The era of the calendar (1 for AD, 2 for BS).
        first_day_of_month (int): The day of the week (1-7) for the first day of the month.
        last_day_of_month (int): The day of the week (1-7) for the last day of the month.
        total_days_in_month (int): The total number of days in the month.
        day_of_week_in_month (int): The number of times the day of the week occurs in the month
            (e.g., 5 for the fifth Friday of the month). Defaults to -1 if not applicable.
        day_of_week (int): The day of the week (1-7, e.g., 1 for Sunday). Defaults to -1 if not applicable.
        day_of_year (int): The day of the year (1-366). Defaults to -1 if not applicable.
        week_of_month (int): The week of the month (1-5). Defaults to -1 if not applicable.
        week_of_year (int): The week of the year (1-53). Defaults to -1 if not applicable.
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
        
        
@dataclass(frozen=True)
class CustomDateTime:
    """
    A data holder representing a CustomCalendar and SimpleTime.

    Combines a CustomCalendar instance (representing the calendar)
    and a SimpleTime instance (representing the time).

    Attributes:
        custom_calendar (CustomCalendar): The custom calendar represented by CustomCalendar.
        simple_time (SimpleTime): The corresponding time of day represented by SimpleTime.
    """
    custom_calendar: CustomCalendar
    simple_time: SimpleTime
