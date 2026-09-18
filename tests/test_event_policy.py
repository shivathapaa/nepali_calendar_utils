"""A calendar policy: the week an institution keeps, the days it names, and the
status it reports for one day or a whole month."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates
from nepali_calendar_utils.event import (
    NepaliCalendarEvent,
    NepaliCalendarPolicy,
    NepaliDayStatus,
    NepaliEventKind,
    NepaliEventProvider,
    NepaliWeekend,
    NoOpEventProvider,
    add_working_days,
    next_working_day,
    working_days_between,
)

SATURDAY = 7
SUNDAY = 1


class StaticProvider(NepaliEventProvider):
    def __init__(self, *entries):
        self._by_year = {}
        for entry in entries:
            self._by_year.setdefault(entry.date.year, set()).add(entry)

    def events(self, year):
        return self._by_year.get(year, set())


def event(year, month, day, name, kind=NepaliEventKind.GOVERNMENT_PUBLIC, **rest):
    return NepaliCalendarEvent(SimpleDate(year, month, day), name, kind, **rest)


def _cal(year, month, day):
    return NepaliDateConverter.get_nepali_calendar(year, month, day)


def _first_day_of_week(year, month, day, day_of_week, span=15):
    for offset in range(span):
        c = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            year, month, day, offset
        )
        if c.day_of_week == day_of_week:
            return SimpleDate(c.year, c.month, c.day_of_month)
    raise AssertionError(f"no day_of_week={day_of_week} within {span} days")


class TestPolicyConstruction(unittest.TestCase):
    def test_defaults_to_the_nepali_office_week(self):
        policy = NepaliCalendarPolicy()
        self.assertEqual(NepaliWeekend.Default, policy.weekly_off_days)
        self.assertIs(NoOpEventProvider, policy.provider)

    def test_default_singleton_closes_saturdays_and_names_nothing(self):
        default = NepaliCalendarPolicy.Default
        self.assertEqual(frozenset({SATURDAY}), default.weekly_off_days)
        self.assertEqual([], default.events_in(2082, 1))
        saturday = _first_day_of_week(2082, 1, 1, SATURDAY)
        self.assertTrue(default.is_non_working_day(saturday))
        self.assertFalse(default.is_non_working_day(_first_day_of_week(2082, 1, 1, SUNDAY)))

    def test_any_iterable_is_kept_as_a_frozenset(self):
        policy = NepaliCalendarPolicy([SATURDAY, SUNDAY, SATURDAY])
        self.assertEqual(frozenset({SATURDAY, SUNDAY}), policy.weekly_off_days)

    def test_empty_week_never_closes_for_the_week_alone(self):
        policy = NepaliCalendarPolicy(frozenset())
        self.assertFalse(any(policy.is_weekly_off(day) for day in range(1, 8)))

    def test_a_week_that_never_opens(self):
        policy = NepaliCalendarPolicy(frozenset(range(1, 8)))
        self.assertTrue(all(policy.is_weekly_off(day) for day in range(1, 8)))

    def test_rejects_a_day_that_is_not_a_day_of_the_week(self):
        for strays in ([0], [8], [-1], [SATURDAY, 0]):
            with self.assertRaises(ValueError, msg=f"accepted {strays}"):
                NepaliCalendarPolicy(frozenset(strays))

    def test_rejection_names_the_stray_numbers(self):
        with self.assertRaises(ValueError) as caught:
            NepaliCalendarPolicy(frozenset({0, SATURDAY}))
        self.assertIn("0", str(caught.exception))


class TestPolicyQueries(unittest.TestCase):
    def setUp(self):
        self.public = event(2082, 1, 1, "New Year", NepaliEventKind.GOVERNMENT_PUBLIC)
        self.observance = event(2082, 1, 1, "Office tea", NepaliEventKind.OBSERVANCE)
        self.regional = event(2082, 1, 5, "Jatra", NepaliEventKind.REGIONAL)
        self.other_month = event(2082, 2, 3, "Mela", NepaliEventKind.REGIONAL)
        self.policy = NepaliCalendarPolicy(
            provider=StaticProvider(
                self.observance, self.public, self.regional, self.other_month
            )
        )

    def test_events_on_orders_by_kind(self):
        on_new_year = self.policy.events_on(SimpleDate(2082, 1, 1))
        self.assertEqual(["New Year", "Office tea"], [e.name for e in on_new_year])

    def test_events_on_unnamed_day_is_empty(self):
        self.assertEqual([], self.policy.events_on(SimpleDate(2082, 1, 2)))

    def test_events_on_uncovered_year_is_empty(self):
        self.assertEqual([], self.policy.events_on(SimpleDate(2070, 1, 1)))

    def test_events_in_is_date_then_kind_ordered(self):
        names = [e.name for e in self.policy.events_in(2082, 1)]
        self.assertEqual(["New Year", "Office tea", "Jatra"], names)

    def test_events_in_ignores_other_months(self):
        self.assertEqual(["Mela"], [e.name for e in self.policy.events_in(2082, 2)])

    def test_events_in_empty_month(self):
        self.assertEqual([], self.policy.events_in(2082, 3))

    def test_status_of_reports_events_and_derived_fields(self):
        status = self.policy.status_of(SimpleDate(2082, 1, 1))
        self.assertEqual(["New Year", "Office tea"], status.names)
        self.assertEqual(NepaliEventKind.GOVERNMENT_PUBLIC, status.primary_kind)
        self.assertEqual(["New Year"], [e.name for e in status.closures])
        self.assertTrue(status.is_non_working)

    def test_status_of_plain_day(self):
        status = self.policy.status_of(SimpleDate(2082, 1, 2))
        self.assertEqual((), status.events)
        self.assertIsNone(status.primary_kind)
        self.assertEqual([], status.closures)

    def test_status_of_weekly_off_day_carries_no_kind(self):
        saturday = _first_day_of_week(2082, 1, 1, SATURDAY)
        status = NepaliCalendarPolicy().status_of(saturday)
        self.assertTrue(status.is_weekly_off)
        self.assertTrue(status.is_non_working)
        self.assertIsNone(status.primary_kind)

    def test_is_non_working_day(self):
        self.assertTrue(self.policy.is_non_working_day(SimpleDate(2082, 1, 1)))
        self.assertTrue(self.policy.is_non_working_day(SimpleDate(2082, 1, 5)))
        self.assertFalse(self.policy.is_non_working_day(SimpleDate(2082, 1, 2)))

    def test_a_day_carrying_only_an_observance_is_worked(self):
        policy = NepaliCalendarPolicy(
            frozenset(), StaticProvider(event(2082, 1, 2, "Tea", NepaliEventKind.OBSERVANCE))
        )
        self.assertFalse(policy.is_non_working_day(SimpleDate(2082, 1, 2)))

    def test_is_non_working_day_hears_a_provider_that_answers_directly(self):
        class AlwaysClosed(NepaliEventProvider):
            def events(self, year):
                return set()

            def closes_on(self, date):
                return True

        policy = NepaliCalendarPolicy(frozenset(), AlwaysClosed())
        self.assertTrue(policy.is_non_working_day(SimpleDate(2082, 1, 2)))


class TestMonthStatus(unittest.TestCase):
    def setUp(self):
        self.policy = NepaliCalendarPolicy(
            provider=StaticProvider(
                event(2082, 1, 1, "New Year"),
                event(2082, 1, 1, "Office tea", NepaliEventKind.OBSERVANCE),
                event(2082, 1, 15, "Jatra", NepaliEventKind.REGIONAL),
            )
        )

    def test_one_entry_per_day_of_the_month(self):
        expected = NepaliDateConverter.get_nepali_month_calendar(2082, 1).total_days_in_month
        self.assertEqual(expected, len(self.policy.month_status(2082, 1)))

    def test_events_land_on_the_right_day(self):
        statuses = self.policy.month_status(2082, 1)
        self.assertEqual(["New Year", "Office tea"], statuses[0].names)
        self.assertEqual(["Jatra"], statuses[14].names)
        self.assertEqual([], statuses[1].names)

    def test_agrees_with_status_of_for_every_day(self):
        for year, month in ((2082, 1), (2082, 12), (2000, 6), (1970, 1), (2100, 12)):
            policy = NepaliCalendarPolicy(frozenset({SATURDAY, SUNDAY}))
            statuses = policy.month_status(year, month)
            for index, status in enumerate(statuses):
                date = SimpleDate(year, month, index + 1)
                self.assertEqual(
                    policy.status_of(date).is_weekly_off,
                    status.is_weekly_off,
                    f"{date} disagreed about the week",
                )

    def test_walks_the_week_across_the_supported_range(self):
        policy = NepaliCalendarPolicy()
        first_year = NepaliCalendarDefaults.NepaliYearRange.start
        last_year = NepaliCalendarDefaults.NepaliYearRange.stop - 1
        for year in range(first_year, last_year + 1, 10):
            for month in (1, 6, 12):
                statuses = policy.month_status(year, month)
                offs = sum(1 for status in statuses if status.is_weekly_off)
                self.assertIn(offs, (4, 5), f"{year}-{month} had {offs} Saturdays")

    def test_a_year_the_provider_does_not_cover_is_all_unnamed(self):
        statuses = self.policy.month_status(2083, 1)
        self.assertTrue(all(status.events == () for status in statuses))


class TestDayStatus(unittest.TestCase):
    def test_working_constant(self):
        self.assertFalse(NepaliDayStatus.Working.is_weekly_off)
        self.assertEqual((), NepaliDayStatus.Working.events)
        self.assertFalse(NepaliDayStatus.Working.is_non_working)
        self.assertIsNone(NepaliDayStatus.Working.primary_kind)

    def test_a_sequence_of_events_is_kept_as_a_tuple(self):
        status = NepaliDayStatus(False, [event(2082, 1, 1, "New Year")])
        self.assertIsInstance(status.events, tuple)

    def test_weekly_off_alone_is_non_working(self):
        self.assertTrue(NepaliDayStatus(True, ()).is_non_working)

    def test_observance_alone_is_working(self):
        status = NepaliDayStatus(
            False, (event(2082, 1, 1, "Tea", NepaliEventKind.OBSERVANCE),)
        )
        self.assertFalse(status.is_non_working)
        self.assertEqual([], status.closures)


class TestPolicyAsSelectableDates(unittest.TestCase):
    def setUp(self):
        self.policy = NepaliCalendarPolicy(
            provider=StaticProvider(
                event(2082, 1, 2, "Bida"),
                event(2082, 1, 3, "Programme", NepaliEventKind.OBSERVANCE),
            )
        )
        self.selectable = self.policy.as_selectable_dates()

    def test_blocks_a_closed_day(self):
        self.assertFalse(self.selectable.is_selectable_date(_cal(2082, 1, 2)))

    def test_keeps_a_day_that_stays_open(self):
        self.assertTrue(self.selectable.is_selectable_date(_cal(2082, 1, 3)))

    def test_blocks_the_weekly_off_day(self):
        saturday = _first_day_of_week(2082, 1, 1, SATURDAY)
        self.assertFalse(
            self.selectable.is_selectable_date(
                _cal(saturday.year, saturday.month, saturday.day_of_month)
            )
        )

    def test_years_stay_selectable(self):
        self.assertTrue(self.selectable.is_selectable_year(2082))

    def test_a_week_that_never_opens_blocks_every_day(self):
        selectable = NepaliCalendarPolicy(frozenset(range(1, 8))).as_selectable_dates()
        for day in range(1, 8):
            self.assertFalse(selectable.is_selectable_date(_cal(2082, 1, day)))

    def test_composes_with_a_converter_rule(self):
        after = NepaliDateConverter.after_date_selectable(SimpleDate(2082, 1, 10))
        from nepali_calendar_utils.event import excluding_closures

        combined = excluding_closures(after, self.policy.provider)
        self.assertFalse(combined.is_selectable_date(_cal(2082, 1, 5)))
        self.assertTrue(combined.is_selectable_date(_cal(2082, 1, 11)))


class TestPolicyArithmetic(unittest.TestCase):
    """A policy given to the working-day helpers answers what its two parts answer."""

    def setUp(self):
        self.provider = StaticProvider(
            event(2082, 1, 3, "Bida"), event(2082, 1, 9, "Bida")
        )
        self.start = SimpleDate(2082, 1, 1)
        self.end = SimpleDate(2082, 2, 1)

    def test_matches_the_provider_form(self):
        for week in (frozenset(), frozenset({SATURDAY}), frozenset({SUNDAY, SATURDAY})):
            policy = NepaliCalendarPolicy(week, self.provider)
            self.assertEqual(
                working_days_between(self.start, self.end, self.provider, weekend=week),
                working_days_between(self.start, self.end, policy),
                f"counts disagreed for {sorted(week)}",
            )
            self.assertEqual(
                next_working_day(self.start, self.provider, weekend=week),
                next_working_day(self.start, policy),
            )
            self.assertEqual(
                add_working_days(self.start, 12, self.provider, weekend=week),
                add_working_days(self.start, 12, policy),
            )

    def test_the_converter_facade_takes_a_policy(self):
        policy = NepaliCalendarPolicy(provider=self.provider)
        self.assertEqual(
            working_days_between(self.start, self.end, policy),
            NepaliDateConverter.working_days_between(self.start, self.end, policy),
        )

    def test_a_policy_and_a_weekend_together_are_rejected(self):
        policy = NepaliCalendarPolicy(provider=self.provider)
        with self.assertRaises(ValueError):
            working_days_between(self.start, self.end, policy, weekend=frozenset())
        with self.assertRaises(ValueError):
            next_working_day(self.start, policy, weekend=frozenset())
        with self.assertRaises(ValueError):
            add_working_days(self.start, 1, policy, weekend=frozenset())

    def test_merged_providers_under_one_policy(self):
        national = StaticProvider(event(2082, 1, 3, "National bida"))
        local = StaticProvider(event(2082, 1, 4, "Local bida"))
        policy = NepaliCalendarPolicy(frozenset(), national + local)
        self.assertTrue(policy.is_non_working_day(SimpleDate(2082, 1, 3)))
        self.assertTrue(policy.is_non_working_day(SimpleDate(2082, 1, 4)))
        self.assertFalse(policy.is_non_working_day(SimpleDate(2082, 1, 5)))


if __name__ == "__main__":
    unittest.main()
