"""The holiday package under its former name.

Importing anything from here raises a :class:`DeprecationWarning` and hands back the
matching name from :mod:`nepali_calendar_utils.event`, where a holiday is one kind of
calendar event among festivals, programmes and deadlines. Code written against these
names keeps working, implementations of ``NepaliHolidayProvider`` included.
"""

import warnings

from nepali_calendar_utils.holiday.holiday_provider import (
    HolidayKind,
    HolidayEntry,
    NepaliHolidayProvider,
    NoOpHolidayProvider,
    NepaliWeekend,
)
from nepali_calendar_utils.holiday.holiday_helpers import (
    excluding_holidays,
    excluding_weekends,
    working_days_between,
    next_working_day,
    add_working_days,
)

warnings.warn(
    "nepali_calendar_utils.holiday is the former name of nepali_calendar_utils.event, "
    "where a holiday is one kind of calendar event. Import NepaliCalendarEvent, "
    "NepaliEventKind, NepaliEventProvider, NoOpEventProvider and excluding_closures "
    "from nepali_calendar_utils instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "HolidayKind",
    "HolidayEntry",
    "NepaliHolidayProvider",
    "NoOpHolidayProvider",
    "NepaliWeekend",
    "excluding_holidays",
    "excluding_weekends",
    "working_days_between",
    "next_working_day",
    "add_working_days",
]
