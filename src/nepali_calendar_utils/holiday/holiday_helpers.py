"""The picker wrappers and working-day arithmetic under their former names.

Each name here resolves to its counterpart in
:mod:`nepali_calendar_utils.event.event_helpers`, which takes a calendar policy as
well as a provider.
"""

from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates
from nepali_calendar_utils.event.event_helpers import (
    add_working_days,
    excluding_closures,
    excluding_weekends,
    next_working_day,
    working_days_between,
)
from nepali_calendar_utils.event.nepali_event_provider import NepaliEventProvider


def excluding_holidays(
    base: NepaliSelectableDates, provider: NepaliEventProvider
) -> NepaliSelectableDates:
    """Former name of
    :func:`~nepali_calendar_utils.event.event_helpers.excluding_closures`, which is
    what it does: an event that leaves the institution open no longer blocks its day.

    A provider written against :class:`
    ~nepali_calendar_utils.holiday.holiday_provider.NepaliHolidayProvider` blocks
    every entry it lists, as it always did.
    """
    return excluding_closures(base, provider)


__all__ = [
    "excluding_holidays",
    "excluding_weekends",
    "working_days_between",
    "next_working_day",
    "add_working_days",
]
