"""The former holiday names: what still resolves, what a provider written against
them still answers, and the warning that says where they moved."""

import unittest
import warnings

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.event import (
    NepaliCalendarEvent,
    NepaliCalendarPolicy,
    NepaliEventKind,
    NepaliEventProvider,
    NoOpEventProvider,
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from nepali_calendar_utils.holiday import (
        HolidayEntry,
        HolidayKind,
        NepaliHolidayProvider,
        NoOpHolidayProvider,
        NepaliWeekend,
        excluding_holidays,
        excluding_weekends,
        working_days_between,
        next_working_day,
        add_working_days,
    )


class MyHolidays(NepaliHolidayProvider):
    """A provider as it would have been written before the rename."""

    def holidays(self, year):
        if year != 2082:
            return set()
        return {
            HolidayEntry(SimpleDate(2082, 1, 1), "New Year", HolidayKind.GOVERNMENT_PUBLIC),
            HolidayEntry(SimpleDate(2082, 1, 3), "Health Day", HolidayKind.OBSERVANCE),
        }


class TestFormerNames(unittest.TestCase):
    def test_the_types_are_the_current_ones(self):
        self.assertIs(NepaliCalendarEvent, HolidayEntry)
        self.assertIs(NepaliEventKind, HolidayKind)

    def test_the_kind_members_are_unchanged(self):
        self.assertEqual("government_public", HolidayKind.GOVERNMENT_PUBLIC.value)
        self.assertEqual(
            {"GOVERNMENT_PUBLIC", "RELIGIOUS", "REGIONAL", "OBSERVANCE"},
            {kind.name for kind in HolidayKind},
        )

    def test_an_entry_still_takes_three_positional_arguments(self):
        entry = HolidayEntry(SimpleDate(2082, 1, 1), "New Year", HolidayKind.RELIGIOUS)
        self.assertEqual(SimpleDate(2082, 1, 1), entry.date)
        self.assertEqual("New Year", entry.name)
        self.assertEqual(HolidayKind.RELIGIOUS, entry.kind)

    def test_the_weekend_default_is_unchanged(self):
        self.assertEqual(frozenset({7}), NepaliWeekend.Default)

    def test_the_package_root_still_resolves_them(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            import nepali_calendar_utils

            self.assertIs(HolidayEntry, nepali_calendar_utils.HolidayEntry)
            self.assertIs(NepaliHolidayProvider, nepali_calendar_utils.NepaliHolidayProvider)

    def test_they_are_no_longer_part_of_the_documented_surface(self):
        import nepali_calendar_utils

        self.assertNotIn("HolidayEntry", nepali_calendar_utils.__all__)
        self.assertIn("NepaliCalendarEvent", nepali_calendar_utils.__all__)

    def test_an_unknown_name_still_fails(self):
        import nepali_calendar_utils

        with self.assertRaises(AttributeError):
            nepali_calendar_utils.NotAName

    def test_importing_the_package_warns(self):
        import importlib
        import sys

        # A fresh import is the only way to see an import-time warning again. The
        # modules and the attribute on the package are put back afterwards, or every
        # later test would be comparing against a second copy of the same classes.
        import nepali_calendar_utils

        loaded = {
            name: module
            for name, module in sys.modules.items()
            if name.startswith("nepali_calendar_utils.holiday")
        }
        for name in loaded:
            del sys.modules[name]
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                importlib.import_module("nepali_calendar_utils.holiday")
        finally:
            sys.modules.update(loaded)
            nepali_calendar_utils.holiday = loaded["nepali_calendar_utils.holiday"]

        categories = [warning.category for warning in caught]
        self.assertIn(DeprecationWarning, categories)
        self.assertIn("nepali_calendar_utils.event", str(caught[0].message))


class TestFormerProviderStillWorks(unittest.TestCase):
    def setUp(self):
        self.provider = MyHolidays()

    def test_its_own_methods_answer(self):
        self.assertTrue(self.provider.is_holiday(SimpleDate(2082, 1, 1)))
        self.assertFalse(self.provider.is_holiday(SimpleDate(2082, 1, 2)))
        self.assertEqual(2, len(self.provider.holidays(2082)))

    def test_it_is_an_event_provider(self):
        self.assertIsInstance(self.provider, NepaliEventProvider)
        self.assertEqual(self.provider.holidays(2082), self.provider.events(2082))

    def test_every_listed_entry_still_closes_its_day(self):
        # The older rule: an entry blocks the day whatever its kind says.
        self.assertTrue(self.provider.closes_on(SimpleDate(2082, 1, 3)))

    def test_it_drives_a_policy(self):
        policy = NepaliCalendarPolicy(frozenset(), self.provider)
        self.assertTrue(policy.is_non_working_day(SimpleDate(2082, 1, 1)))
        self.assertTrue(policy.is_non_working_day(SimpleDate(2082, 1, 3)))
        self.assertFalse(policy.is_non_working_day(SimpleDate(2082, 1, 2)))

    def test_its_entries_read_back_through_the_policy(self):
        policy = NepaliCalendarPolicy(provider=self.provider)
        self.assertEqual(["New Year"], policy.status_of(SimpleDate(2082, 1, 1)).names)
        self.assertEqual(2, len(policy.events_in(2082, 1)))

    def test_it_composes_with_a_current_provider(self):
        class Extra(NepaliEventProvider):
            def events(self, year):
                return {
                    NepaliCalendarEvent(
                        SimpleDate(2082, 1, 9), "Jatra", NepaliEventKind.REGIONAL
                    )
                }

        combined = self.provider + Extra()
        self.assertEqual(3, len(combined.events(2082)))
        self.assertTrue(combined.closes_on(SimpleDate(2082, 1, 3)))
        self.assertTrue(combined.closes_on(SimpleDate(2082, 1, 9)))

    def test_the_no_op_answers_both_vocabularies(self):
        self.assertEqual(set(), NoOpHolidayProvider.holidays(2082))
        self.assertEqual(set(), NoOpHolidayProvider.events(2082))
        self.assertFalse(NoOpHolidayProvider.is_holiday(SimpleDate(2082, 1, 1)))
        self.assertFalse(NoOpHolidayProvider.closes_on(SimpleDate(2082, 1, 1)))


class TestFormerHelpers(unittest.TestCase):
    def test_excluding_holidays_blocks_what_the_provider_lists(self):
        wrapped = excluding_holidays(NepaliSelectableDates(), MyHolidays())
        self.assertFalse(
            wrapped.is_selectable_date(NepaliDateConverter.get_nepali_calendar(2082, 1, 1))
        )
        self.assertTrue(
            wrapped.is_selectable_date(NepaliDateConverter.get_nepali_calendar(2082, 1, 2))
        )

    def test_excluding_weekends_is_the_same_function(self):
        from nepali_calendar_utils.event import excluding_weekends as current

        self.assertIs(current, excluding_weekends)

    def test_the_arithmetic_is_the_same_function(self):
        from nepali_calendar_utils.event import (
            add_working_days as current_add,
            next_working_day as current_next,
            working_days_between as current_between,
        )

        self.assertIs(current_between, working_days_between)
        self.assertIs(current_next, next_working_day)
        self.assertIs(current_add, add_working_days)

    def test_the_arithmetic_still_takes_the_old_provider(self):
        start = SimpleDate(2082, 1, 1)
        end = SimpleDate(2082, 1, 8)
        self.assertEqual(
            working_days_between(start, end, MyHolidays()),
            working_days_between(start, end, MyHolidays(), weekend=NepaliWeekend.Default),
        )
        self.assertGreater(next_working_day(start, MyHolidays()), start)
        self.assertGreater(add_working_days(start, 1, NoOpEventProvider), start)


if __name__ == "__main__":
    unittest.main()
