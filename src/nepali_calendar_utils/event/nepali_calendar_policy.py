"""When one institution is closed, and what its calendar has on it."""

from dataclasses import dataclass
from typing import FrozenSet, List

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates
from nepali_calendar_utils.event.event_helpers import excluding_closures, excluding_weekends
from nepali_calendar_utils.event.nepali_calendar_event import NepaliCalendarEvent
from nepali_calendar_utils.event.nepali_day_status import NepaliDayStatus
from nepali_calendar_utils.event.nepali_event_provider import (
    NepaliEventProvider,
    NepaliWeekend,
    NoOpEventProvider,
)

DAYS_IN_WEEK = 7


@dataclass(frozen=True)
class NepaliCalendarPolicy:
    """The days of the week an institution never opens, plus the events it keeps.

    The two travel together because they answer the same question, and an app that
    states them once gets both a calendar that paints the right days and arithmetic
    that counts the right ones. An office in Nepal is
    ``NepaliCalendarPolicy(provider=my_events)``, closed Saturdays. A school closed
    Saturday and Sunday is ``NepaliCalendarPolicy(frozenset({7, 1}), my_events)``.
    Two institutions with different lists are two policies over two providers, and a
    national list shared by both is ``national + own_list``.

    Nothing here blocks a date on its own. :meth:`as_selectable_dates` turns the
    policy into a picker rule when that is what you want, so marking a day and
    refusing it stay separate decisions.

    Attributes:
        weekly_off_days (frozenset[int]): Days of the week the institution is closed,
            1 for Sunday through 7 for Saturday. Defaults to ``NepaliWeekend.Default``,
            the single Saturday weekend Nepal observes. An empty set is an institution
            that never closes for the week alone. Any iterable may be passed in; it is
            kept as a frozenset.
        provider (NepaliEventProvider): The events the institution keeps. Defaults to
            ``NoOpEventProvider``, which is the right value while an app has only its
            weekly rule wired.

    Raises:
        ValueError: if ``weekly_off_days`` holds a number that is not a day of the
            week. Other calendars number Sunday 0, and a set written to that
            convention would quietly close nothing, so it is rejected at construction
            rather than at the end of a month of wrong answers.
    """

    weekly_off_days: FrozenSet[int] = NepaliWeekend.Default
    provider: NepaliEventProvider = NoOpEventProvider

    def __post_init__(self):
        days = frozenset(self.weekly_off_days)
        strays = sorted(day for day in days if not 1 <= day <= DAYS_IN_WEEK)
        if strays:
            raise ValueError(
                "weekly_off_days must hold days of the week, 1 for Sunday through 7 for "
                f"Saturday, but got {strays}"
            )
        object.__setattr__(self, "weekly_off_days", days)

    def is_weekly_off(self, day_of_week: int) -> bool:
        """Whether ``day_of_week`` (1 for Sunday through 7 for Saturday) is one of the
        institution's weekly off days.

        Takes the day of the week rather than a date because a calendar grid already
        knows it, and resolving it again would cost a conversion per cell.
        """
        return day_of_week in self.weekly_off_days

    def events_on(self, date: SimpleDate) -> List[NepaliCalendarEvent]:
        """The events on ``date``, strongest kind first, or an empty list when the day
        carries none. A weekly off day with nothing named on it answers empty."""
        return sorted(
            (event for event in self.provider.events(date.year) if event.date == date),
            key=lambda event: event.kind.priority,
        )

    def events_in(self, year: int, month: int) -> List[NepaliCalendarEvent]:
        """Every event in the Bikram Sambat month ``month`` of ``year``, in date order
        and, within a date, strongest kind first.

        Empty for a month with none, and for a year the provider does not cover.
        """
        return sorted(
            (event for event in self.provider.events(year) if event.date.month == month),
            key=lambda event: (event.date.day_of_month, event.kind.priority),
        )

    def status_of(self, date: SimpleDate) -> NepaliDayStatus:
        """What ``date`` is under this policy: whether the week makes it a day off, and
        what is named on it.

        Resolves the day of the week through the conversion table, so prefer
        :meth:`month_status` when laying out a whole month.
        """
        from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

        day_of_week = NepaliDateConverter.get_nepali_calendar(
            date.year, date.month, date.day_of_month
        ).day_of_week
        return NepaliDayStatus(
            is_weekly_off=self.is_weekly_off(day_of_week), events=tuple(self.events_on(date))
        )

    def month_status(self, year: int, month: int) -> List[NepaliDayStatus]:
        """Every day of one Bikram Sambat month, in day order: index 0 is day 1.

        The month's first weekday is resolved once and the week walked forward from
        it, so a grid or an agenda costs one conversion rather than one per day.
        """
        from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

        month_calendar = NepaliDateConverter.get_nepali_month_calendar(year, month)
        events_by_day = {}
        for event in self.events_in(year, month):
            events_by_day.setdefault(event.date.day_of_month, []).append(event)

        statuses = []
        for day_of_month in range(1, month_calendar.total_days_in_month + 1):
            day_of_week = (
                (month_calendar.first_day_of_month - 1 + day_of_month - 1) % DAYS_IN_WEEK
            ) + 1
            statuses.append(
                NepaliDayStatus(
                    is_weekly_off=self.is_weekly_off(day_of_week),
                    events=tuple(events_by_day.get(day_of_month, ())),
                )
            )
        return statuses

    def is_non_working_day(self, date: SimpleDate) -> bool:
        """Whether the institution is closed on ``date``, for either reason.

        A day that is both a weekly off day and a holiday is closed once, and a day
        carrying only an observance is still worked. The provider is asked directly
        rather than through :meth:`status_of`, so one that answers ``closes_on``
        without listing the event behind it is still heard, and this agrees with what
        the working-day helpers count.
        """
        from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

        day_of_week = NepaliDateConverter.get_nepali_calendar(
            date.year, date.month, date.day_of_month
        ).day_of_week
        return self.is_weekly_off(day_of_week) or self.provider.closes_on(date)

    def as_selectable_dates(self) -> NepaliSelectableDates:
        """The policy as a picker rule: every closed day becomes unselectable.

        Opt in to this when a screen should refuse the days it marks, and leave it out
        when the days are only to be seen. An event that does not close the
        institution, a school programme or a meeting, leaves its day selectable, since
        the day is still worked.
        """
        return excluding_closures(
            excluding_weekends(NepaliSelectableDates(), self.weekly_off_days), self.provider
        )


#: Nepal's usual office week: Saturday off, no event data wired yet.
NepaliCalendarPolicy.Default = NepaliCalendarPolicy()
