from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import *
from nepali_calendar_utils.data.calendar_system import CalendarSystem
from nepali_calendar_utils.data.custom_calendar import *
from nepali_calendar_utils.data.month_calendar import MonthCalendar
from nepali_calendar_utils.data.nepali_date_locale import *
from nepali_calendar_utils.data.digit_script import (
    DigitScript,
    default_digit_script,
    latin_digit_or_none,
    to_latin_digits,
)
from nepali_calendar_utils.data.nepali_date_formatter import NepaliDateFormatter, DatePattern
from nepali_calendar_utils.data.nepali_time_formatter import NepaliTimeFormatter
from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates
from nepali_calendar_utils.event import (
    NepaliCalendarEvent,
    NepaliEventKind,
    NepaliEventProvider,
    NoOpEventProvider,
    NepaliWeekend,
    NepaliDayStatus,
    NepaliCalendarPolicy,
    excluding_closures,
    excluding_weekends,
    working_days_between,
    next_working_day,
    add_working_days,
)

__all__ = [
    # Locale / formatting enums and holders
    "NameFormat",
    "NepaliDateFormatStyle",
    "NepaliWeekdayName",
    "NepaliMonthName",
    "NepaliCalendarUtilsLang",
    "NepaliDateLocale",
    "NepaliCalendarDefaults",
    # Core data holders
    "CustomCalendar",
    "SimpleDate",
    "SimpleTime",
    "NepaliMonthCalendar",
    "MonthCalendar",
    "CalendarSystem",
    "CustomDateTime",
    # Main facade
    "NepaliDateConverter",
    # Digit scripts
    "DigitScript",
    "default_digit_script",
    "latin_digit_or_none",
    "to_latin_digits",
    # Text-field formatter and the time-of-day wire form
    "NepaliDateFormatter",
    "DatePattern",
    "NepaliTimeFormatter",
    # Selectable dates
    "NepaliSelectableDates",
    # Calendar events, day status and working-day arithmetic
    "NepaliCalendarEvent",
    "NepaliEventKind",
    "NepaliEventProvider",
    "NoOpEventProvider",
    "NepaliWeekend",
    "NepaliDayStatus",
    "NepaliCalendarPolicy",
    "excluding_closures",
    "excluding_weekends",
    "working_days_between",
    "next_working_day",
    "add_working_days",
]

_FORMER_HOLIDAY_NAMES = frozenset(
    {
        "HolidayKind",
        "HolidayEntry",
        "NepaliHolidayProvider",
        "NoOpHolidayProvider",
        "excluding_holidays",
    }
)


def __getattr__(name):
    """Resolve the former holiday names from the package root.

    They are no longer part of ``__all__``, so a star import brings in the event
    surface alone, but ``from nepali_calendar_utils import HolidayEntry`` still works
    and warns. Kept out of the eager imports above so that importing the package
    costs nothing for code that has moved on.
    """
    if name in _FORMER_HOLIDAY_NAMES:
        from nepali_calendar_utils import holiday

        return getattr(holiday, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
