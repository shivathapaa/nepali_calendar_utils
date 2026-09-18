"""A named day in the Bikram Sambat calendar, and the spans built from one."""

from dataclasses import dataclass, replace
from enum import Enum
from typing import List, Optional

from nepali_calendar_utils.data.custom_calendar import SimpleDate


class NepaliEventKind(Enum):
    """What kind of thing an event is, which is what a calendar colors by.

    Deliberately narrow, because adding a case is a breaking change. An app with
    its own taxonomy picks the closest kind and keeps its own category in
    :attr:`NepaliCalendarEvent.payload`; whether the day is worked is
    :attr:`NepaliCalendarEvent.closes_offices`'s job either way.
    """

    #: Bank / government office is closed. Sarkari bida.
    GOVERNMENT_PUBLIC = "government_public"

    #: Religious or cultural: Dashain, Tihar, Holi, Id, Christmas, and the like.
    RELIGIOUS = "religious"

    #: Province- or district-level, not nationally observed.
    REGIONAL = "regional"

    #: Recognized but ordinarily worked: World Health Day, a school programme, a meeting.
    OBSERVANCE = "observance"

    @property
    def priority(self) -> int:
        """How strongly a kind describes a day when several land on it, lowest first.

        A day the offices close is called that before anything else it also happens
        to be, and an observance yields to everything. Sorting and color resolution
        both read this, so the two never disagree.
        """
        return _PRIORITY_BY_KIND[self]

    @property
    def closes_offices_by_default(self) -> bool:
        """Whether an event of this kind usually shuts the institution.

        This is what :attr:`NepaliCalendarEvent.closes_offices` falls back to. Only a
        starting point: the event itself has the final say, because the same kind
        closes one place and not another.
        """
        return _CLOSES_OFFICES_BY_KIND[self]


_PRIORITY_BY_KIND = {
    NepaliEventKind.GOVERNMENT_PUBLIC: 0,
    NepaliEventKind.RELIGIOUS: 1,
    NepaliEventKind.REGIONAL: 2,
    NepaliEventKind.OBSERVANCE: 3,
}

_CLOSES_OFFICES_BY_KIND = {
    NepaliEventKind.GOVERNMENT_PUBLIC: True,
    NepaliEventKind.RELIGIOUS: True,
    NepaliEventKind.REGIONAL: True,
    NepaliEventKind.OBSERVANCE: False,
}


@dataclass(frozen=True)
class NepaliCalendarEvent:
    """Something that happens on one Bikram Sambat day.

    A public holiday, a festival, a school programme, a deadline, a birthday. A
    holiday is an event like any other; what separates them is ``closes_offices``,
    not the name: two days can both be called Dashain and only one of them close the
    school. That is why the flag lives here rather than on ``kind``, where a taxonomy
    would have to decide for every institution at once.

    Attributes:
        date (SimpleDate): Bikram Sambat date the event falls on. One day per entry,
            so a ten-day festival is ten entries, which :meth:`spanning_days` and
            :meth:`spanning_through` build from one.
        name (str): Display name, for example "Dashain - Vijaya Dashami" or "Sprint
            review".
        kind (NepaliEventKind): Category, which is what a calendar colors by.
        closes_offices (bool): Whether the institution is shut for this. Leave it
            unset (``None``) to take what ``kind`` usually means, so a
            ``GOVERNMENT_PUBLIC`` entry closes the day and an ``OBSERVANCE`` does
            not; the attribute is a plain ``bool`` once constructed. Either default
            can be overridden: a regional holiday closes one district and not the
            next, and a school programme closes nothing at all.
        id (str): An identifier the app can correlate back to its own record, carried
            through untouched. The library never reads it.
        payload (str): Anything else the app wants back when the day is tapped, as an
            opaque string: JSON, a URL, an identifier list. The library never parses
            it.
    """

    date: SimpleDate
    name: str
    kind: NepaliEventKind
    closes_offices: Optional[bool] = None
    id: Optional[str] = None
    payload: Optional[str] = None

    def __post_init__(self):
        if self.closes_offices is None:
            object.__setattr__(self, "closes_offices", self.kind.closes_offices_by_default)

    def spanning_days(self, days: int) -> List["NepaliCalendarEvent"]:
        """This event on each of ``days`` consecutive days, starting on its own date.

        A :class:`NepaliCalendarEvent` covers a single day, so a span is a list of
        entries rather than a range. Every entry keeps this event's ``name``,
        ``kind``, ``closes_offices``, ``id`` and ``payload``, and differs only in its
        date. A span running out of Chaitra into Baisakh yields entries in both
        years, so each one is reported by the year a provider is asked for.

        Give the event an ``id`` first when the days have to be recognized as one
        thing again. Nepal's published holiday lists name each day separately, so
        prefer real per-day names where they exist and keep this for a span an app
        owns.

        The event's own date is taken as stated, the way every other call here treats
        it, so only the length of the span is checked.

        Args:
            days (int): How many days the span covers, counting the first. ``1``
                returns this event alone.

        Returns:
            list[NepaliCalendarEvent]: One entry per day, in date order.

        Raises:
            ValueError: if ``days`` is below 1, or if the span runs past
                ``NepaliCalendarDefaults.NepaliYearRange``.
        """
        from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

        if days < 1:
            raise ValueError(f"days must be at least 1, but was {days}")

        span = [self]
        for offset in range(1, days):
            moved = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
                self.date.year, self.date.month, self.date.day_of_month, offset
            )
            span.append(
                replace(self, date=SimpleDate(moved.year, moved.month, moved.day_of_month))
            )
        return span

    def spanning_through(self, end: SimpleDate) -> List["NepaliCalendarEvent"]:
        """This event on each day from its own date through ``end``, both included.

        That is the shape published holiday lists and leave requests usually state a
        span in. Expands the same way :meth:`spanning_days` does: an entry per day,
        carrying everything but the date unchanged. An ``end`` equal to this event's
        date returns the event alone.

        Args:
            end (SimpleDate): Last day of the span, included.

        Returns:
            list[NepaliCalendarEvent]: One entry per day, in date order.

        Raises:
            ValueError: if ``end`` falls before this event's date, if ``end`` is not a
                day its month has, or if the span runs past
                ``NepaliCalendarDefaults.NepaliYearRange``. A day the month does not
                reach is refused rather than rolled into the next one, since rolling
                would silently return a span of the wrong length.
        """
        from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

        if end < self.date:
            raise ValueError(f"end ({end}) must be on or after the event's date ({self.date})")

        days_in_end_month = NepaliDateConverter.get_nepali_month_calendar(
            end.year, end.month
        ).total_days_in_month
        if not 1 <= end.day_of_month <= days_in_end_month:
            raise ValueError(
                f"end ({end}) is not a day of its month, which has {days_in_end_month} days"
            )

        return self.spanning_days(
            NepaliDateConverter.get_nepali_days_in_between(self.date, end) + 1
        )
