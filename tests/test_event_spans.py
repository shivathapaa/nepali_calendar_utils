"""An event that runs longer than a day: what the expanded entries carry, where a
span is refused, and how it reads back through a provider and a policy."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.event import (
    NepaliCalendarEvent,
    NepaliCalendarPolicy,
    NepaliEventKind,
    NepaliEventProvider,
    next_working_day,
    working_days_between,
)

DASHAIN_DAYS = 10


def add_days(date, days):
    moved = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
        date.year, date.month, date.day_of_month, days
    )
    return SimpleDate(moved.year, moved.month, moved.day_of_month)


def dashain(year=2082, month=6, day=17, **rest):
    return NepaliCalendarEvent(
        SimpleDate(year, month, day), "Dashain", NepaliEventKind.RELIGIOUS, **rest
    )


class SpanProvider(NepaliEventProvider):
    """Reports a span the way a real provider does: by the year each entry falls in."""

    def __init__(self, *events):
        self._by_year = {}
        for entry in events:
            self._by_year.setdefault(entry.date.year, set()).add(entry)

    def events(self, year):
        return self._by_year.get(year, set())


class TestSpanningDays(unittest.TestCase):
    def test_one_entry_per_day(self):
        span = dashain().spanning_days(DASHAIN_DAYS)
        self.assertEqual(DASHAIN_DAYS, len(span))

    def test_days_are_consecutive_and_in_order(self):
        span = dashain().spanning_days(DASHAIN_DAYS)
        for index, entry in enumerate(span):
            self.assertEqual(add_days(span[0].date, index), entry.date)

    def test_one_day_returns_the_event_alone(self):
        event = dashain()
        self.assertEqual([event], event.spanning_days(1))

    def test_the_first_entry_is_the_event_itself(self):
        event = dashain()
        self.assertIs(event, event.spanning_days(4)[0])

    def test_every_other_field_is_carried(self):
        event = dashain(closes_offices=False, id="dashain-2082", payload='{"n":1}')
        for entry in event.spanning_days(5):
            self.assertEqual(event.name, entry.name)
            self.assertEqual(event.kind, entry.kind)
            self.assertEqual(False, entry.closes_offices)
            self.assertEqual("dashain-2082", entry.id)
            self.assertEqual('{"n":1}', entry.payload)

    def test_a_closing_default_survives_expansion(self):
        for entry in dashain().spanning_days(3):
            self.assertTrue(entry.closes_offices)

    def test_an_id_makes_the_span_one_thing_again(self):
        span = dashain(id="dashain-2082").spanning_days(DASHAIN_DAYS)
        self.assertEqual({"dashain-2082"}, {entry.id for entry in span})

    def test_crossing_a_month_end(self):
        days_in_month = NepaliDateConverter.get_nepali_month_calendar(
            2082, 6
        ).total_days_in_month
        event = dashain(day=days_in_month - 1)
        span = event.spanning_days(4)
        self.assertEqual([6, 6, 7, 7], [entry.date.month for entry in span])

    def test_crossing_a_year_end(self):
        days_in_chaitra = NepaliDateConverter.get_nepali_month_calendar(
            2082, 12
        ).total_days_in_month
        event = dashain(month=12, day=days_in_chaitra)
        span = event.spanning_days(3)
        self.assertEqual([2082, 2083, 2083], [entry.date.year for entry in span])
        self.assertEqual([12, 1, 1], [entry.date.month for entry in span])

    def test_zero_or_negative_days_is_refused(self):
        for days in (0, -1, -10):
            with self.assertRaises(ValueError, msg=f"accepted {days}"):
                dashain().spanning_days(days)

    def test_the_event_date_is_taken_as_given(self):
        # Only the length of the span is checked, the way every other call here
        # treats the date it is handed.
        event = NepaliCalendarEvent(
            SimpleDate(2082, 1, 32), "Odd", NepaliEventKind.OBSERVANCE
        )
        self.assertEqual([event], event.spanning_days(1))

    def test_running_past_the_supported_range_is_refused(self):
        last_year = NepaliCalendarDefaults.NepaliYearRange.stop - 1
        days_in_chaitra = NepaliDateConverter.get_nepali_month_calendar(
            last_year, 12
        ).total_days_in_month
        event = dashain(year=last_year, month=12, day=days_in_chaitra)
        with self.assertRaises(ValueError):
            event.spanning_days(3)

    def test_holds_across_the_supported_range(self):
        first_year = NepaliCalendarDefaults.NepaliYearRange.start
        last_year = NepaliCalendarDefaults.NepaliYearRange.stop - 1
        for year in range(first_year, last_year, 7):
            for month in (1, 6, 12):
                span = dashain(year=year, month=month, day=1).spanning_days(9)
                self.assertEqual(9, len(span))
                self.assertEqual(
                    8, NepaliDateConverter.get_nepali_days_in_between(span[0].date, span[-1].date)
                )


class TestSpanningThrough(unittest.TestCase):
    def test_both_ends_are_included(self):
        span = dashain().spanning_through(SimpleDate(2082, 6, 26))
        self.assertEqual(DASHAIN_DAYS, len(span))
        self.assertEqual(SimpleDate(2082, 6, 17), span[0].date)
        self.assertEqual(SimpleDate(2082, 6, 26), span[-1].date)

    def test_the_same_day_returns_the_event_alone(self):
        event = dashain()
        self.assertEqual([event], event.spanning_through(event.date))

    def test_agrees_with_spanning_days(self):
        event = dashain()
        by_length = event.spanning_days(DASHAIN_DAYS)
        by_end = event.spanning_through(by_length[-1].date)
        self.assertEqual(by_length, by_end)

    def test_crossing_a_year_end(self):
        event = dashain(month=12, day=25)
        span = event.spanning_through(SimpleDate(2083, 1, 5))
        self.assertEqual([2082, 2083], sorted({entry.date.year for entry in span}))

    def test_an_end_before_the_event_is_refused(self):
        with self.assertRaises(ValueError):
            dashain().spanning_through(SimpleDate(2082, 6, 16))

    def test_a_day_the_month_does_not_have_is_refused(self):
        days_in_month = NepaliDateConverter.get_nepali_month_calendar(
            2082, 6
        ).total_days_in_month
        with self.assertRaises(ValueError) as caught:
            dashain().spanning_through(SimpleDate(2082, 6, days_in_month + 1))
        self.assertIn(str(days_in_month), str(caught.exception))

    def test_a_day_below_one_is_refused(self):
        # Ordered after the event's date, so this reaches the day-of-month check.
        with self.assertRaises(ValueError):
            dashain(month=6, day=1).spanning_through(SimpleDate(2082, 7, 0))

    def test_a_month_the_calendar_does_not_have_is_refused(self):
        with self.assertRaises(ValueError):
            dashain().spanning_through(SimpleDate(2082, 13, 1))


class TestSpansThroughAProvider(unittest.TestCase):
    def setUp(self):
        self.span = dashain(id="dashain-2082").spanning_days(DASHAIN_DAYS)
        self.policy = NepaliCalendarPolicy(provider=SpanProvider(*self.span))

    def test_every_day_of_the_span_is_named(self):
        for entry in self.span:
            self.assertEqual(["Dashain"], self.policy.status_of(entry.date).names)

    def test_the_month_reports_the_whole_span(self):
        self.assertEqual(DASHAIN_DAYS, len(self.policy.events_in(2082, 6)))

    def test_an_id_collapses_the_span_to_one_agenda_row(self):
        rows = {entry.id for entry in self.policy.events_in(2082, 6)}
        self.assertEqual({"dashain-2082"}, rows)

    def test_the_span_closes_every_one_of_its_days(self):
        for entry in self.span:
            self.assertTrue(self.policy.is_non_working_day(entry.date))

    def test_the_day_after_the_span_is_worked_again(self):
        after = add_days(self.span[-1].date, 1)
        status = self.policy.status_of(after)
        self.assertEqual([], status.names)

    def test_a_span_that_does_not_close_leaves_its_days_worked(self):
        leave = NepaliCalendarEvent(
            SimpleDate(2082, 6, 17), "Sprint", NepaliEventKind.OBSERVANCE
        ).spanning_days(5)
        policy = NepaliCalendarPolicy(frozenset(), SpanProvider(*leave))
        self.assertFalse(policy.is_non_working_day(leave[0].date))
        self.assertEqual(["Sprint"], policy.status_of(leave[0].date).names)

    def test_a_span_crossing_the_year_is_reported_by_both_years(self):
        crossing = dashain(month=12, day=25).spanning_days(DASHAIN_DAYS)
        provider = SpanProvider(*crossing)
        in_2082 = len(provider.events(2082))
        in_2083 = len(provider.events(2083))
        self.assertEqual(DASHAIN_DAYS, in_2082 + in_2083)
        self.assertTrue(in_2082 and in_2083)

    def test_the_arithmetic_counts_the_span_off(self):
        start = self.span[0].date
        end = add_days(self.span[-1].date, 1)
        self.assertEqual(0, working_days_between(start, end, self.policy))

    def test_the_next_working_day_lands_after_the_span(self):
        after = next_working_day(self.span[0].date, self.policy)
        self.assertGreater(after, self.span[-1].date)

    def test_a_span_of_one_day_behaves_like_a_single_event(self):
        single = dashain().spanning_days(1)
        policy = NepaliCalendarPolicy(provider=SpanProvider(*single))
        self.assertEqual(1, len(policy.events_in(2082, 6)))


if __name__ == "__main__":
    unittest.main()
