"""What one day is under a calendar policy."""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from nepali_calendar_utils.event.nepali_calendar_event import (
    NepaliCalendarEvent,
    NepaliEventKind,
)


@dataclass(frozen=True)
class NepaliDayStatus:
    """Whether the week makes a day off, and what is named on it.

    The two are kept apart because they answer different questions. A weekly off day
    repeats fifty-two times a year and carries no name worth drawing; an event is a
    fact about that date alone. A day can be both, and a day that is both is still
    one day off, so :attr:`is_non_working` is a single answer rather than a count.

    Attributes:
        is_weekly_off (bool): Whether the day falls on one of the policy's weekly off
            days.
        events (tuple[NepaliCalendarEvent, ...]): Everything named on the day,
            strongest :class:`NepaliEventKind` first. Empty when the day carries
            nothing, which is the usual case even for a weekly off day. Any sequence
            may be passed in; it is kept as a tuple.
    """

    is_weekly_off: bool
    events: Tuple[NepaliCalendarEvent, ...] = field(default=())

    def __post_init__(self):
        if not isinstance(self.events, tuple):
            object.__setattr__(self, "events", tuple(self.events))

    @property
    def is_non_working(self) -> bool:
        """True when the institution is shut, whether the week says so or an event does.

        Only an event that closes offices counts, so a working day carrying a
        programme or a meeting stays a working day, and the working-day helpers
        agree.
        """
        return self.is_weekly_off or any(event.closes_offices for event in self.events)

    @property
    def primary_kind(self) -> Optional[NepaliEventKind]:
        """The kind that describes the day best, or ``None`` when nothing is named on it.

        A day that is only a weekly off day has no kind, which is what separates "it
        is Saturday" from "it is Dashain, which happens to be a Saturday".
        """
        return self.events[0].kind if self.events else None

    @property
    def names(self) -> List[str]:
        """The names of the day's events, strongest first, for whatever the app draws
        or announces."""
        return [event.name for event in self.events]

    @property
    def closures(self) -> List[NepaliCalendarEvent]:
        """The events that actually shut the institution, the subset the arithmetic
        counts."""
        return [event for event in self.events if event.closes_offices]


#: An ordinary working day: no weekly rule, nothing named.
NepaliDayStatus.Working = NepaliDayStatus(is_weekly_off=False, events=())
