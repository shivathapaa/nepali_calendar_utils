import unittest

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates
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


class StaticProvider(NepaliHolidayProvider):
    def __init__(self, *entries):
        self._by_year = {}
        for entry in entries:
            self._by_year.setdefault(entry.date.year, set()).add(entry)

    def holidays(self, year):
        return self._by_year.get(year, set())


def cal(year, month, day):
    return NepaliDateConverter.get_nepali_calendar(year, month, day)


def add_days(date, days):
    result = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
        date.year, date.month, date.day_of_month, days
    )
    return SimpleDate(result.year, result.month, result.day_of_month)


class TestHolidayProvider(unittest.TestCase):
    def test_is_holiday(self):
        provider = StaticProvider(
            HolidayEntry(SimpleDate(2082, 1, 1), "New Year", HolidayKind.GOVERNMENT_PUBLIC)
        )
        self.assertTrue(provider.is_holiday(SimpleDate(2082, 1, 1)))
        self.assertFalse(provider.is_holiday(SimpleDate(2082, 1, 2)))

    def test_noop_provider(self):
        self.assertEqual(set(), NoOpHolidayProvider.holidays(2082))
        self.assertFalse(NoOpHolidayProvider.is_holiday(SimpleDate(2082, 1, 1)))

    def test_holiday_entry_hashable(self):
        entry = HolidayEntry(SimpleDate(2082, 1, 1), "New Year", HolidayKind.RELIGIOUS)
        self.assertIn(entry, {entry})


class TestWorkingDays(unittest.TestCase):
    def setUp(self):
        self.start = SimpleDate(2081, 1, 1)
        self.end7 = add_days(self.start, 7)

    def test_zero_span(self):
        self.assertEqual(0, working_days_between(self.start, self.start, NoOpHolidayProvider))

    def test_week_has_exactly_one_saturday(self):
        # Any 7-day window contains exactly one Saturday (day_of_week == 7).
        self.assertEqual(6, working_days_between(self.start, self.end7, NoOpHolidayProvider))

    def test_holiday_in_window_reduces_count(self):
        # Mark a non-Saturday day inside the window as a holiday.
        holiday_date = None
        for offset in range(7):
            c = cal(self.start.year, self.start.month, self.start.day_of_month) if offset == 0 \
                else NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
                    self.start.year, self.start.month, self.start.day_of_month, offset)
            if c.day_of_week != 7:
                holiday_date = SimpleDate(c.year, c.month, c.day_of_month)
                break
        provider = StaticProvider(HolidayEntry(holiday_date, "Bida", HolidayKind.GOVERNMENT_PUBLIC))
        self.assertEqual(5, working_days_between(self.start, self.end7, provider))

    def test_start_after_end_raises(self):
        with self.assertRaises(ValueError):
            working_days_between(self.end7, self.start, NoOpHolidayProvider)

    def test_next_working_day_on_working_day_returns_self(self):
        # 2081-05-24 is English 2024-09-09, a Monday (not Saturday).
        d = SimpleDate(2081, 5, 24)
        self.assertEqual(d, next_working_day(d, NoOpHolidayProvider))

    def test_next_working_day_skips_saturday(self):
        # Find a Saturday, then assert next_working_day advances past it.
        saturday = None
        for offset in range(14):
            c = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 1, 1, offset)
            if c.day_of_week == 7:
                saturday = SimpleDate(c.year, c.month, c.day_of_month)
                break
        result = next_working_day(saturday, NoOpHolidayProvider)
        result_cal = cal(result.year, result.month, result.day_of_month)
        self.assertNotEqual(7, result_cal.day_of_week)
        self.assertEqual(add_days(saturday, 1), result)

    def test_add_working_days_zero(self):
        d = SimpleDate(2081, 1, 1)
        self.assertEqual(d, add_working_days(d, 0, NoOpHolidayProvider))

    def test_add_working_days_no_weekend_equals_plain_add(self):
        d = SimpleDate(2081, 1, 1)
        self.assertEqual(add_days(d, 10), add_working_days(d, 10, NoOpHolidayProvider, weekend=frozenset()))

    def test_add_working_days_negative(self):
        d = SimpleDate(2081, 5, 15)
        self.assertEqual(add_days(d, -10), add_working_days(d, -10, NoOpHolidayProvider, weekend=frozenset()))

    def test_add_working_days_skips_saturday(self):
        # With Saturday-only weekend, add_working_days must never land on a Saturday.
        d = SimpleDate(2081, 1, 1)
        for n in range(1, 12):
            result = add_working_days(d, n, NoOpHolidayProvider)
            c = cal(result.year, result.month, result.day_of_month)
            self.assertNotEqual(7, c.day_of_week, f"landed on Saturday for n={n}")


class TestSelectableWrappers(unittest.TestCase):
    def test_excluding_weekends(self):
        wrapped = excluding_weekends(NepaliSelectableDates())
        # Find a Saturday and a non-Saturday.
        saturday = non_saturday = None
        for offset in range(14):
            c = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 1, 1, offset)
            if c.day_of_week == 7 and saturday is None:
                saturday = c
            elif c.day_of_week != 7 and non_saturday is None:
                non_saturday = c
        self.assertFalse(wrapped.is_selectable_date(saturday))
        self.assertTrue(wrapped.is_selectable_date(non_saturday))

    def test_excluding_holidays(self):
        provider = StaticProvider(
            HolidayEntry(SimpleDate(2082, 1, 1), "New Year", HolidayKind.GOVERNMENT_PUBLIC)
        )
        wrapped = excluding_holidays(NepaliSelectableDates(), provider)
        self.assertFalse(wrapped.is_selectable_date(cal(2082, 1, 1)))
        self.assertTrue(wrapped.is_selectable_date(cal(2082, 1, 2)))

    def test_converter_working_day_facade(self):
        # The facade methods delegate to the same helpers.
        start = SimpleDate(2081, 1, 1)
        end = add_days(start, 7)
        self.assertEqual(6, NepaliDateConverter.working_days_between(start, end, NoOpHolidayProvider))


if __name__ == "__main__":
    unittest.main()
