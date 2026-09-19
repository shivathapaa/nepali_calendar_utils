"""Service-provider interface for supplying a calendar's events.

This library ships **no data** by design: Nepali holiday lists change year to year
and every institution keeps its own, so nothing here could be right for long.
Implement :class:`NepaliEventProvider` with your own source (a static map, a CMS, an
HR API) and hand it to
:class:`~nepali_calendar_utils.event.nepali_calendar_policy.NepaliCalendarPolicy`.
"""

from typing import Callable, Set

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.event.nepali_calendar_event import NepaliCalendarEvent


class NepaliEventProvider:
    """Interface for supplying the events a calendar names: holidays, festivals,
    programmes, anything an app wants written on a day.

    Implementations must:
      - return a stable set for a given ``year`` (calling twice yields the same
        contents),
      - not raise for years outside the supported Nepali year range, returning an
        empty set instead.

    Example::

        class MyEvents(NepaliEventProvider):
            _by_year = {
                2082: {
                    NepaliCalendarEvent(SimpleDate(2082, 1, 1), "नयाँ वर्ष",
                                        NepaliEventKind.GOVERNMENT_PUBLIC),
                },
            }
            def events(self, year):
                return self._by_year.get(year, set())
    """

    def events(self, year: int) -> Set[NepaliCalendarEvent]:
        """Everything named in ``year`` (BS). An empty set is a valid answer."""
        raise NotImplementedError

    def closes_on(self, date: SimpleDate) -> bool:
        """Whether the institution is shut on ``date``, which is what the working-day
        helpers count by.

        The default answers from :meth:`events`, counting only the entries whose
        ``closes_offices`` is set, so a day carrying nothing but an observance is
        still a working day. Override with a memoized implementation if you call this
        in tight loops.
        """
        return any(
            event.date == date and event.closes_offices for event in self.events(date.year)
        )

    def __add__(self, other: "NepaliEventProvider") -> "NepaliEventProvider":
        """A provider reporting everything either side reports, which is how a
        national list and an institution's own list are put together.

        A date named by both sides keeps both entries, so a day can be a public
        holiday nationally and something else locally without one hiding the other.
        A day either side calls a closure stays a closure, including when that side
        answers by overriding :meth:`closes_on` rather than by listing an event.
        """
        if not isinstance(other, NepaliEventProvider):
            return NotImplemented
        return _CombinedEventProvider(self, other)

    def filtered(
        self, predicate: Callable[[NepaliCalendarEvent], bool]
    ) -> "NepaliEventProvider":
        """A view of this provider carrying only the entries ``predicate`` accepts.

        For narrowing a shared list to what one screen cares about::

            provider.filtered(lambda e: e.kind is NepaliEventKind.GOVERNMENT_PUBLIC)

        ``predicate`` runs on every entry of a year each time that year is asked for,
        so keep it a test rather than a lookup.

        A day stays closed while a closure behind it survives the filter, so narrowing
        a list narrows the closures with it. A day the source shuts without naming a
        closing event stays shut, since there is nothing to narrow.
        ``filtered(lambda e: True)`` therefore answers exactly what the source does.
        """
        return _FilteredEventProvider(self, predicate)


class _CombinedEventProvider(NepaliEventProvider):
    def __init__(self, first: NepaliEventProvider, second: NepaliEventProvider):
        self._first = first
        self._second = second

    def events(self, year: int) -> Set[NepaliCalendarEvent]:
        return set(self._first.events(year)) | set(self._second.events(year))

    def closes_on(self, date: SimpleDate) -> bool:
        return self._first.closes_on(date) or self._second.closes_on(date)


class _FilteredEventProvider(NepaliEventProvider):
    def __init__(
        self, source: NepaliEventProvider, predicate: Callable[[NepaliCalendarEvent], bool]
    ):
        self._source = source
        self._predicate = predicate

    def events(self, year: int) -> Set[NepaliCalendarEvent]:
        return {event for event in self._source.events(year) if self._predicate(event)}

    def closes_on(self, date: SimpleDate) -> bool:
        if not self._source.closes_on(date):
            return False
        closures = [
            event
            for event in self._source.events(date.year)
            if event.date == date and event.closes_offices
        ]
        return not closures or any(self._predicate(event) for event in closures)


class _NoOpEventProvider(NepaliEventProvider):
    """Behaves as if nothing is ever named and nothing ever closes."""

    def events(self, year: int) -> Set[NepaliCalendarEvent]:
        return set()

    def closes_on(self, date: SimpleDate) -> bool:
        return False


#: No-op provider singleton. Use when you want the event-aware APIs but have not
#: wired a data source yet.
NoOpEventProvider = _NoOpEventProvider()


class NepaliWeekend:
    """Day-of-week conventions.

    The library uses a 1-based-Sunday convention everywhere: Sunday = 1, ...,
    Saturday = 7.
    """

    #: Default weekend in Nepal: Saturday only. Nepal observes a single-day weekend,
    #: so working-day arithmetic that uses this matches what a Nepali office counts
    #: as "5 working days from today". Pass ``frozenset({6, 7})`` for a Friday-and-
    #: Saturday weekend.
    Default = frozenset({7})
