"""Mirrors the Kotlin core CalendarPropertiesTests."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

ALL_YEARS = NepaliCalendarDefaults.NepaliYearRange


class TestEnglishMonthLengths(unittest.TestCase):
    def test_february_common_year_has_28(self):
        self.assertEqual(28, NepaliDateConverter.get_total_days_in_english_month(2023, 2))

    def test_february_div_by_4_has_29(self):
        self.assertEqual(29, NepaliDateConverter.get_total_days_in_english_month(2024, 2))

    def test_february_div_by_100_not_400_has_28(self):
        self.assertEqual(28, NepaliDateConverter.get_total_days_in_english_month(1900, 2))

    def test_february_div_by_400_has_29(self):
        self.assertEqual(29, NepaliDateConverter.get_total_days_in_english_month(2000, 2))

    def test_thirty_day_months(self):
        for month in (4, 6, 9, 11):
            self.assertEqual(30, NepaliDateConverter.get_total_days_in_english_month(2024, month))

    def test_thirty_one_day_months(self):
        for month in (1, 3, 5, 7, 8, 10, 12):
            self.assertEqual(31, NepaliDateConverter.get_total_days_in_english_month(2024, month))

    def test_invalid_month_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_total_days_in_english_month(2024, 0)
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_total_days_in_english_month(2024, 13)


class TestNepaliMonthLengths(unittest.TestCase):
    def test_min_year_month_one(self):
        self.assertEqual(31, NepaliDateConverter.get_total_days_in_nepali_month(1970, 1))

    def test_max_year_month_twelve(self):
        self.assertEqual(31, NepaliDateConverter.get_total_days_in_nepali_month(2100, 12))

    def test_2082_month3_has_32(self):
        self.assertEqual(32, NepaliDateConverter.get_total_days_in_nepali_month(2082, 3))

    def test_all_months_in_range_29_to_32(self):
        for year in ALL_YEARS:
            for month in range(1, 13):
                days = NepaliDateConverter.get_total_days_in_nepali_month(year, month)
                self.assertIn(days, range(29, 33), f"{year}-{month} has {days} days")

    def test_year_totals_in_364_to_367(self):
        for year in ALL_YEARS:
            total = sum(NepaliDateConverter.get_total_days_in_nepali_month(year, m) for m in range(1, 13))
            self.assertIn(total, range(364, 368), f"{year} total {total}")

    def test_year_outside_table_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_total_days_in_nepali_month(1500, 1)

    def test_invalid_month_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_total_days_in_nepali_month(2081, 0)
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_total_days_in_nepali_month(2081, 13)


class TestMonthCalendar(unittest.TestCase):
    def test_month_calendar_matches_first_day_calendar(self):
        cal = NepaliDateConverter.get_nepali_calendar(2081, 5, 1)
        month = NepaliDateConverter.get_nepali_month_calendar(2081, 5)
        self.assertEqual(cal.year, month.year)
        self.assertEqual(cal.month, month.month)
        self.assertEqual(cal.first_day_of_month, month.first_day_of_month)
        self.assertEqual(cal.last_day_of_month, month.last_day_of_month)
        self.assertEqual(cal.total_days_in_month, month.total_days_in_month)

    def test_first_and_last_day_in_range_one_to_seven(self):
        for year in range(2080, 2091):
            for month in range(1, 13):
                m = NepaliDateConverter.get_nepali_month_calendar(year, month)
                self.assertIn(m.first_day_of_month, range(1, 8))
                self.assertIn(m.last_day_of_month, range(1, 8))

    def test_consecutive_months_first_day_chain(self):
        for year in range(2080, 2086):
            for month in range(1, 12):
                current = NepaliDateConverter.get_nepali_month_calendar(year, month)
                nxt = NepaliDateConverter.get_nepali_month_calendar(year, month + 1)
                expected_next_first = (current.last_day_of_month % 7) + 1
                self.assertEqual(expected_next_first, nxt.first_day_of_month,
                                 f"weekday chain broken {year}-{month} -> {month + 1}")

    def test_invalid_month_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_month_calendar(2081, 0)
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_month_calendar(2081, 13)


class TestGetNepaliCalendarFields(unittest.TestCase):
    def test_first_day_of_year_day_of_year_is_one(self):
        self.assertEqual(1, NepaliDateConverter.get_nepali_calendar(2081, 1, 1).day_of_year)

    def test_day_of_year_increases_by_one_each_day(self):
        previous = NepaliDateConverter.get_nepali_calendar(2081, 1, 1)
        for i in range(1, 31):
            nxt = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 1, 1, i)
            self.assertEqual(previous.day_of_year + 1, nxt.day_of_year)
            previous = nxt

    def test_last_day_of_year_day_of_year_matches_total(self):
        total = sum(NepaliDateConverter.get_total_days_in_nepali_month(2081, m) for m in range(1, 13))
        last_day = NepaliDateConverter.get_total_days_in_nepali_month(2081, 12)
        cal = NepaliDateConverter.get_nepali_calendar(2081, 12, last_day)
        self.assertEqual(total, cal.day_of_year)

    def test_day_of_week_walks_one_to_seven_and_wraps(self):
        first = NepaliDateConverter.get_nepali_calendar(2081, 1, 1).day_of_week
        for i in range(1, 22):
            cal = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 1, 1, i)
            expected = ((first - 1 + i) % 7) + 1
            self.assertEqual(expected, cal.day_of_week, f"after {i} days")

    def test_invalid_day_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_calendar(2081, 5, 50)

    def test_invalid_month_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_calendar(2081, 13, 1)
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_calendar(2081, 0, 1)


if __name__ == "__main__":
    unittest.main()
