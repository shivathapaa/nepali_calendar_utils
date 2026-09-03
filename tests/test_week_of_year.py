"""Mirrors the Kotlin core WeekOfYearTests.

The weekly fields only mean anything if the weekday is right, so day-of-week and
day-of-year are first pinned to sources outside this library (the Gregorian date
via the stdlib ``datetime.date``, and the raw month-length table). The
``week_of_year`` invariants then rest on a trusted weekday.
"""

import unittest
from datetime import date

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

SAMPLE_YEARS = [1970, 1971, 2000, 2050, 2080, 2081, 2082, 2099, 2100]
ALL_YEARS = NepaliCalendarDefaults.NepaliYearRange


def _calendar(year, month, day):
    return NepaliDateConverter.get_nepali_calendar(year, month, day)


def _days_in_month(year, month):
    return NepaliDateConverter.get_total_days_in_nepali_month(year, month)


def _each_day(year):
    for month in range(1, 13):
        for day in range(1, _days_in_month(year, month) + 1):
            yield month, day


class TestWeekOfYear(unittest.TestCase):
    def test_day_of_week_matches_gregorian_calendar(self):
        # Independent oracle: convert each BS date to Gregorian and ask the stdlib for the
        # weekday. Library uses 1=Sunday..7=Saturday; ISO uses 1=Monday..7=Sunday.
        for year in SAMPLE_YEARS:
            for month, day in _each_day(year):
                cal = _calendar(year, month, day)
                greg = NepaliDateConverter.convert_nepali_to_english(year, month, day)
                iso_from_calendar = 7 if cal.day_of_week == 1 else cal.day_of_week - 1
                iso_from_gregorian = date(greg.year, greg.month, greg.day_of_month).isoweekday()
                self.assertEqual(iso_from_gregorian, iso_from_calendar,
                                 f"weekday mismatch at BS {year}/{month}/{day}")

    def test_day_of_year_matches_running_month_length_sum(self):
        for year in SAMPLE_YEARS:
            for month, day in _each_day(year):
                expected = sum(_days_in_month(year, m) for m in range(1, month)) + day
                self.assertEqual(expected, _calendar(year, month, day).day_of_year,
                                 f"dayOfYear at {year}/{month}/{day}")

    def test_baisakh_first_is_always_week_one(self):
        for year in ALL_YEARS:
            self.assertEqual(1, _calendar(year, 1, 1).week_of_year, f"Baisakh 1, {year}")

    def test_week_advances_only_after_saturday(self):
        # Independent of the calculate_week_of_year formula: the week number advances by one
        # exactly when the previous day was Saturday (day_of_week 7).
        for year in SAMPLE_YEARS:
            previous_week = 0
            previous_dow = 0
            first = True
            for month, day in _each_day(year):
                cal = _calendar(year, month, day)
                if first:
                    self.assertEqual(1, cal.week_of_year, f"first day of {year}")
                    first = False
                else:
                    expected = previous_week + 1 if previous_dow == 7 else previous_week
                    self.assertEqual(expected, cal.week_of_year, f"weekOfYear at {year}/{month}/{day}")
                previous_week = cal.week_of_year
                previous_dow = cal.day_of_week

    def test_last_day_of_every_year_is_week_52_to_54_and_max_is_54(self):
        global_max = 0
        for year in ALL_YEARS:
            last_week = _calendar(year, 12, _days_in_month(year, 12)).week_of_year
            self.assertIn(last_week, range(52, 55), f"year {year} ends week {last_week}")
            global_max = max(global_max, last_week)
        self.assertEqual(54, global_max, "some year should reach week 54")

    def test_week_of_year_matches_day_of_year_and_year_start_weekday(self):
        # Regression lock on the exact formula: ceil((dayOfYear + weekdayOfBaisakh1 - 1) / 7).
        for year in (2080, 2081, 2082):
            start_weekday = _calendar(year, 1, 1).day_of_week
            for month, day in _each_day(year):
                cal = _calendar(year, month, day)
                days_passed = cal.day_of_year + (start_weekday - 1)
                expected = (days_passed + 6) // 7
                self.assertEqual(expected, cal.week_of_year, f"formula mismatch at {year}/{month}/{day}")


if __name__ == "__main__":
    unittest.main()
