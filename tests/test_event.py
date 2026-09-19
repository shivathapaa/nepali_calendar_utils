"""The event provider SPI, the picker wrappers over it, and working-day arithmetic."""

import unittest

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates
from nepali_calendar_utils.event import (
    NepaliCalendarEvent,
    NepaliEventKind,
    NepaliEventProvider,
    NoOpEventProvider,
    NepaliWeekend,
    excluding_closures,
    excluding_weekends,
    working_days_between,
    next_working_day,
    add_working_days,
)


class StaticProvider(NepaliEventProvider):
    def __init__(self, *entries):
        self._by_year = {}
        for entry in entries:
            self._by_year.setdefault(entry.date.year, set()).add(entry)

    def events(self, year):
        return self._by_year.get(year, set())


class AlwaysClosedProvider(NepaliEventProvider):
    """Pathological provider that answers closes_on without listing an event."""

    def events(self, year):
        return set()

    def closes_on(self, date):
        return True


class OnlyEvenDaysSelectable(NepaliSelectableDates):
    def is_selectable_date(self, custom_calendar):
        return custom_calendar.day_of_month % 2 == 0


def cal(year, month, day):
    return NepaliDateConverter.get_nepali_calendar(year, month, day)


def add_days(date, days):
    result = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
        date.year, date.month, date.day_of_month, days
    )
    return SimpleDate(result.year, result.month, result.day_of_month)


def first_day_of_week(year, month, day, day_of_week, span=15):
    """The first date at or after the given one that falls on ``day_of_week``."""
    for offset in range(span):
        c = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            year, month, day, offset
        )
        if c.day_of_week == day_of_week:
            return SimpleDate(c.year, c.month, c.day_of_month)
    raise AssertionError(f"no day_of_week={day_of_week} within {span} days")


class TestEventProvider(unittest.TestCase):
    def test_closes_on(self):
        provider = StaticProvider(
            NepaliCalendarEvent(
                SimpleDate(2082, 1, 1), "New Year", NepaliEventKind.GOVERNMENT_PUBLIC
            )
        )
        self.assertTrue(provider.closes_on(SimpleDate(2082, 1, 1)))
        self.assertFalse(provider.closes_on(SimpleDate(2082, 1, 2)))

    def test_observance_does_not_close(self):
        provider = StaticProvider(
            NepaliCalendarEvent(
                SimpleDate(2082, 1, 1), "Sprint review", NepaliEventKind.OBSERVANCE
            )
        )
        self.assertFalse(provider.closes_on(SimpleDate(2082, 1, 1)))

    def test_closes_offices_override_beats_the_kind(self):
        open_holiday = NepaliCalendarEvent(
            SimpleDate(2082, 1, 1), "Local bida", NepaliEventKind.REGIONAL, closes_offices=False
        )
        closing_observance = NepaliCalendarEvent(
            SimpleDate(2082, 1, 2), "Annual day", NepaliEventKind.OBSERVANCE, closes_offices=True
        )
        provider = StaticProvider(open_holiday, closing_observance)
        self.assertFalse(provider.closes_on(SimpleDate(2082, 1, 1)))
        self.assertTrue(provider.closes_on(SimpleDate(2082, 1, 2)))

    def test_kind_defaults(self):
        self.assertTrue(NepaliEventKind.GOVERNMENT_PUBLIC.closes_offices_by_default)
        self.assertTrue(NepaliEventKind.RELIGIOUS.closes_offices_by_default)
        self.assertTrue(NepaliEventKind.REGIONAL.closes_offices_by_default)
        self.assertFalse(NepaliEventKind.OBSERVANCE.closes_offices_by_default)

    def test_kind_priorities_are_distinct_and_ordered(self):
        priorities = [kind.priority for kind in NepaliEventKind]
        self.assertEqual(sorted(priorities), priorities)
        self.assertEqual(len(set(priorities)), len(priorities))
        self.assertEqual(0, NepaliEventKind.GOVERNMENT_PUBLIC.priority)

    def test_noop_provider(self):
        self.assertEqual(set(), NoOpEventProvider.events(2082))
        self.assertFalse(NoOpEventProvider.closes_on(SimpleDate(2082, 1, 1)))

    def test_event_hashable(self):
        event = NepaliCalendarEvent(
            SimpleDate(2082, 1, 1), "New Year", NepaliEventKind.RELIGIOUS
        )
        self.assertIn(event, {event})

    def test_identical_events_collapse_in_a_set(self):
        one = NepaliCalendarEvent(SimpleDate(2082, 1, 1), "New Year", NepaliEventKind.RELIGIOUS)
        two = NepaliCalendarEvent(SimpleDate(2082, 1, 1), "New Year", NepaliEventKind.RELIGIOUS)
        self.assertEqual(1, len({one, two}))

    def test_optional_fields_are_carried_untouched(self):
        event = NepaliCalendarEvent(
            SimpleDate(2082, 1, 1),
            "New Year",
            NepaliEventKind.RELIGIOUS,
            id="ny-2082",
            payload='{"url": "https://example.test"}',
        )
        self.assertEqual("ny-2082", event.id)
        self.assertEqual('{"url": "https://example.test"}', event.payload)


class TestProviderComposition(unittest.TestCase):
    def setUp(self):
        self.national = StaticProvider(
            NepaliCalendarEvent(
                SimpleDate(2082, 1, 1), "New Year", NepaliEventKind.GOVERNMENT_PUBLIC
            )
        )
        self.local = StaticProvider(
            NepaliCalendarEvent(SimpleDate(2082, 1, 1), "Jatra", NepaliEventKind.REGIONAL),
            NepaliCalendarEvent(SimpleDate(2082, 1, 5), "Mela", NepaliEventKind.REGIONAL),
        )

    def test_sum_reports_both_sides(self):
        combined = self.national + self.local
        self.assertEqual(3, len(combined.events(2082)))
        self.assertTrue(combined.closes_on(SimpleDate(2082, 1, 5)))

    def test_a_day_named_by_both_keeps_both_entries(self):
        combined = self.national + self.local
        on_new_year = [e for e in combined.events(2082) if e.date == SimpleDate(2082, 1, 1)]
        self.assertEqual(2, len(on_new_year))

    def test_sum_does_not_mutate_either_side(self):
        combined = self.national + self.local
        combined.events(2082)
        self.assertEqual(1, len(self.national.events(2082)))
        self.assertEqual(2, len(self.local.events(2082)))

    def test_sum_with_a_non_provider_is_rejected(self):
        with self.assertRaises(TypeError):
            self.national + object()

    def test_sum_of_empty_providers_is_empty(self):
        combined = NoOpEventProvider + NoOpEventProvider
        self.assertEqual(set(), combined.events(2082))
        self.assertFalse(combined.closes_on(SimpleDate(2082, 1, 1)))

    def test_sum_hears_a_provider_that_answers_closes_on_directly(self):
        combined = NoOpEventProvider + AlwaysClosedProvider()
        self.assertTrue(combined.closes_on(SimpleDate(2082, 1, 1)))

    def test_filtered_narrows_the_entries(self):
        public_only = (self.national + self.local).filtered(
            lambda event: event.kind is NepaliEventKind.GOVERNMENT_PUBLIC
        )
        self.assertEqual(1, len(public_only.events(2082)))
        self.assertFalse(public_only.closes_on(SimpleDate(2082, 1, 5)))

    def test_filtered_does_not_mutate_the_source(self):
        self.national.filtered(lambda event: False).events(2082)
        self.assertEqual(1, len(self.national.events(2082)))

    def test_chained_composition(self):
        chained = (self.national + self.local).filtered(
            lambda event: event.date.day_of_month == 1
        )
        self.assertEqual(2, len(chained.events(2082)))

    def test_filtered_hears_a_provider_that_answers_closes_on_directly(self):
        filtered = AlwaysClosedProvider().filtered(lambda event: True)
        self.assertTrue(filtered.closes_on(SimpleDate(2082, 1, 1)))

    def test_filtered_of_everything_answers_what_the_source_does(self):
        source = self.national + self.local
        identical = source.filtered(lambda event: True)
        for day in (1, 5, 9):
            date = SimpleDate(2082, 1, day)
            self.assertEqual(source.closes_on(date), identical.closes_on(date), date)
        self.assertEqual(source.events(2082), identical.events(2082))

    def test_filtered_keeps_a_closure_whose_event_survived(self):
        date = SimpleDate(2082, 1, 1)
        public_only = (self.national + self.local).filtered(
            lambda event: event.kind is NepaliEventKind.GOVERNMENT_PUBLIC
        )
        self.assertTrue(public_only.closes_on(date))


class TestWorkingDays(unittest.TestCase):
    def setUp(self):
        self.start = SimpleDate(2081, 1, 1)
        self.end7 = add_days(self.start, 7)

    def test_zero_span(self):
        self.assertEqual(0, working_days_between(self.start, self.start, NoOpEventProvider))

    def test_week_has_exactly_one_saturday(self):
        self.assertEqual(6, working_days_between(self.start, self.end7, NoOpEventProvider))

    def test_closure_in_window_reduces_count(self):
        closed = first_day_of_week(2081, 1, 1, 2)  # a Monday inside the window
        provider = StaticProvider(
            NepaliCalendarEvent(closed, "Bida", NepaliEventKind.GOVERNMENT_PUBLIC)
        )
        self.assertEqual(5, working_days_between(self.start, self.end7, provider))

    def test_observance_in_window_does_not_reduce_count(self):
        named = first_day_of_week(2081, 1, 1, 2)
        provider = StaticProvider(
            NepaliCalendarEvent(named, "Programme", NepaliEventKind.OBSERVANCE)
        )
        self.assertEqual(6, working_days_between(self.start, self.end7, provider))

    def test_start_after_end_raises(self):
        with self.assertRaises(ValueError):
            working_days_between(self.end7, self.start, NoOpEventProvider)

    def test_next_working_day_on_working_day_returns_self(self):
        # 2081-05-24 is English 2024-09-09, a Monday (not Saturday).
        d = SimpleDate(2081, 5, 24)
        self.assertEqual(d, next_working_day(d, NoOpEventProvider))

    def test_next_working_day_skips_saturday(self):
        saturday = first_day_of_week(2081, 1, 1, 7)
        result = next_working_day(saturday, NoOpEventProvider)
        result_cal = cal(result.year, result.month, result.day_of_month)
        self.assertNotEqual(7, result_cal.day_of_week)
        self.assertEqual(add_days(saturday, 1), result)

    def test_add_working_days_zero(self):
        d = SimpleDate(2081, 1, 1)
        self.assertEqual(d, add_working_days(d, 0, NoOpEventProvider))

    def test_add_working_days_no_weekend_equals_plain_add(self):
        d = SimpleDate(2081, 1, 1)
        self.assertEqual(
            add_days(d, 10), add_working_days(d, 10, NoOpEventProvider, weekend=frozenset())
        )

    def test_add_working_days_negative(self):
        d = SimpleDate(2081, 5, 15)
        self.assertEqual(
            add_days(d, -10), add_working_days(d, -10, NoOpEventProvider, weekend=frozenset())
        )

    def test_add_working_days_skips_saturday(self):
        d = SimpleDate(2081, 1, 1)
        for n in range(1, 12):
            result = add_working_days(d, n, NoOpEventProvider)
            c = cal(result.year, result.month, result.day_of_month)
            self.assertNotEqual(7, c.day_of_week, f"landed on Saturday for n={n}")


class TestSelectableWrappers(unittest.TestCase):
    def test_excluding_weekends(self):
        wrapped = excluding_weekends(NepaliSelectableDates())
        saturday = first_day_of_week(2081, 1, 1, 7)
        sunday = first_day_of_week(2081, 1, 1, 1)
        self.assertFalse(
            wrapped.is_selectable_date(cal(saturday.year, saturday.month, saturday.day_of_month))
        )
        self.assertTrue(
            wrapped.is_selectable_date(cal(sunday.year, sunday.month, sunday.day_of_month))
        )

    def test_excluding_closures(self):
        provider = StaticProvider(
            NepaliCalendarEvent(
                SimpleDate(2082, 1, 1), "New Year", NepaliEventKind.GOVERNMENT_PUBLIC
            )
        )
        wrapped = excluding_closures(NepaliSelectableDates(), provider)
        self.assertFalse(wrapped.is_selectable_date(cal(2082, 1, 1)))
        self.assertTrue(wrapped.is_selectable_date(cal(2082, 1, 2)))

    def test_excluding_closures_keeps_a_day_that_stays_open(self):
        provider = StaticProvider(
            NepaliCalendarEvent(SimpleDate(2082, 1, 1), "Programme", NepaliEventKind.OBSERVANCE)
        )
        wrapped = excluding_closures(NepaliSelectableDates(), provider)
        self.assertTrue(wrapped.is_selectable_date(cal(2082, 1, 1)))

    def test_converter_working_day_facade(self):
        start = SimpleDate(2081, 1, 1)
        end = add_days(start, 7)
        self.assertEqual(
            6, NepaliDateConverter.working_days_between(start, end, NoOpEventProvider)
        )


class TestWorkingDayEdges(unittest.TestCase):
    """Boundaries of the arithmetic: empty weekends, weeks that never open, year ends."""

    def test_default_weekend_is_saturday_only(self):
        self.assertEqual(frozenset({7}), NepaliWeekend.Default)

    def test_excluding_closures_respects_wrapped_predicate(self):
        wrapped = excluding_closures(OnlyEvenDaysSelectable(), NoOpEventProvider)
        self.assertFalse(wrapped.is_selectable_date(cal(2082, 1, 1)))  # odd
        self.assertTrue(wrapped.is_selectable_date(cal(2082, 1, 2)))   # even

    def test_excluding_weekends_custom_set_rejects_friday_and_saturday(self):
        wrapped = excluding_weekends(NepaliSelectableDates(), weekend=frozenset({6, 7}))
        for offset in range(8):
            c = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
                2082, 1, 1, offset
            )
            expect = c.day_of_week not in (6, 7)
            self.assertEqual(
                expect, wrapped.is_selectable_date(c), f"offset={offset} dow={c.day_of_week}"
            )

    def test_working_days_no_closures_no_weekend_equals_raw_span(self):
        start = SimpleDate(2082, 1, 1)
        end = SimpleDate(2082, 1, 11)  # exclusive, 10 days
        span = NepaliDateConverter.get_nepali_days_in_between(start, end)
        working = working_days_between(start, end, NoOpEventProvider, weekend=frozenset())
        self.assertEqual(span, working)
        self.assertEqual(10, working)

    def test_working_days_default_weekend_skips_two_saturdays_in_14(self):
        start = SimpleDate(2082, 1, 1)
        end = add_days(start, 14)
        self.assertEqual(12, working_days_between(start, end, NoOpEventProvider))

    def test_working_days_closures_skipped(self):
        start = SimpleDate(2082, 1, 1)
        end = SimpleDate(2082, 1, 8)  # 7-day span
        closed = SimpleDate(2082, 1, 3)
        provider = StaticProvider(
            NepaliCalendarEvent(closed, "Bida", NepaliEventKind.GOVERNMENT_PUBLIC)
        )
        raw_span = NepaliDateConverter.get_nepali_days_in_between(start, end)
        weekend_count = 0
        for offset in range(raw_span):
            c = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
                start.year, start.month, start.day_of_month, offset
            )
            if c.day_of_week == 7:
                weekend_count += 1
        expected = raw_span - weekend_count - 1  # the 3rd is a weekday in this window
        self.assertEqual(expected, working_days_between(start, end, provider))

    def test_working_days_closure_on_weekend_not_double_counted(self):
        start = SimpleDate(2082, 1, 1)
        end = SimpleDate(2082, 1, 15)
        saturday = first_day_of_week(2082, 1, 1, 7)
        without = working_days_between(start, end, NoOpEventProvider)
        with_closure = working_days_between(
            start,
            end,
            StaticProvider(
                NepaliCalendarEvent(saturday, "x", NepaliEventKind.GOVERNMENT_PUBLIC)
            ),
        )
        self.assertEqual(without, with_closure)

    def test_working_days_crossing_year_boundary(self):
        start = SimpleDate(2081, 12, 25)
        end = add_days(start, 20)
        self.assertEqual(
            20, working_days_between(start, end, NoOpEventProvider, weekend=frozenset())
        )

    def test_working_days_every_day_off_counts_nothing(self):
        start = SimpleDate(2082, 1, 1)
        end = add_days(start, 20)
        self.assertEqual(
            0,
            working_days_between(
                start, end, NoOpEventProvider, weekend=frozenset(range(1, 8))
            ),
        )

    def test_next_working_day_on_saturday_goes_to_sunday(self):
        saturday = first_day_of_week(2082, 1, 1, 7)
        nxt = next_working_day(saturday, NoOpEventProvider)
        self.assertEqual(1, cal(nxt.year, nxt.month, nxt.day_of_month).day_of_week)

    def test_next_working_day_on_closure_strictly_after(self):
        closed = SimpleDate(2082, 1, 1)
        provider = StaticProvider(
            NepaliCalendarEvent(closed, "x", NepaliEventKind.GOVERNMENT_PUBLIC)
        )
        self.assertGreater(next_working_day(closed, provider), closed)

    def test_next_working_day_all_closed_raises(self):
        with self.assertRaises(RuntimeError):
            next_working_day(SimpleDate(2082, 1, 1), AlwaysClosedProvider(), weekend=frozenset())

    def test_next_working_day_every_weekday_off_raises(self):
        with self.assertRaises(RuntimeError):
            next_working_day(
                SimpleDate(2082, 1, 1), NoOpEventProvider, weekend=frozenset(range(1, 8))
            )

    def test_add_working_days_friday_plus_one_is_sunday(self):
        friday = first_day_of_week(2082, 1, 1, 6)
        nxt = add_working_days(friday, 1, NoOpEventProvider)
        self.assertEqual(1, cal(nxt.year, nxt.month, nxt.day_of_month).day_of_week)

    def test_add_working_days_sunday_minus_one_is_friday(self):
        sunday = first_day_of_week(2082, 1, 1, 1)
        prev = add_working_days(sunday, -1, NoOpEventProvider)
        self.assertEqual(6, cal(prev.year, prev.month, prev.day_of_month).day_of_week)

    def test_add_working_days_skips_closures(self):
        start = SimpleDate(2082, 1, 1)
        next_day = add_days(start, 1)
        provider = StaticProvider(
            NepaliCalendarEvent(next_day, "x", NepaliEventKind.GOVERNMENT_PUBLIC)
        )
        target = add_working_days(start, 1, provider, weekend=frozenset())
        self.assertGreater(target, next_day)

    def test_add_working_days_every_day_off_raises(self):
        with self.assertRaises(RuntimeError):
            add_working_days(
                SimpleDate(2082, 1, 1), 1, NoOpEventProvider, weekend=frozenset(range(1, 8))
            )


if __name__ == "__main__":
    unittest.main()
