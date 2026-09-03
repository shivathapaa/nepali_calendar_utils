import datetime as real_datetime
import unittest
from unittest import mock

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.calendar_model.nepali_calendar_model import NepaliCalendarModel
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.calendar_model.date_converters import DateConverters
import nepali_calendar_utils.calendar_model.nepali_calendar_model as model_module


class TestTodayWallClock(unittest.TestCase):
    """Regression: today_* used to be captured once at construction and never
    rolled over. Now the wall clock is read on every access."""

    def test_today_reads_fresh_each_access(self):
        model = NepaliCalendarModel()
        with mock.patch.object(model_module, "datetime") as dt:
            dt.now.return_value = real_datetime.datetime(2024, 9, 9, 10, 0, 0)
            self.assertEqual(SimpleDate(2024, 9, 9), model.today_english_simple_date)

            # Advance the clock; a fresh read must reflect it (proves not cached).
            dt.now.return_value = real_datetime.datetime(2024, 9, 10, 10, 0, 0)
            self.assertEqual(SimpleDate(2024, 9, 10), model.today_english_simple_date)


class TestWeekOfMonthClamp(unittest.TestCase):
    """Regression: week_of_month was computed from the raw (unclamped) day."""

    def test_clamped_day_used_for_week_of_month(self):
        month_cal = NepaliDateConverter.get_nepali_month_calendar(2081, 6)
        total = month_cal.total_days_in_month

        clamped = DateConverters.get_custom_calendar_using_day_month_year(2081, 6, total + 2, True)
        expected = NepaliDateConverter.get_nepali_calendar(2081, 6, total)

        self.assertEqual(expected.week_of_month, clamped.week_of_month)
        self.assertEqual(expected, clamped)


class TestEnglishAnchorGuard(unittest.TestCase):
    """Regression: English dates before 1913-04-13 silently returned Nepali
    1970-01-01. They must now raise."""

    def test_anchor_converts(self):
        result = NepaliDateConverter.convert_english_to_nepali(1913, 4, 13)
        self.assertEqual((1970, 1, 1), (result.year, result.month, result.day_of_month))

    def test_before_anchor_raises(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(1913, 4, 12)
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(1913, 1, 1)


class TestSimpleDateOrdering(unittest.TestCase):
    def test_comparisons(self):
        a = SimpleDate(2081, 5, 24)
        b = SimpleDate(2081, 5, 25)
        c = SimpleDate(2082, 1, 1)
        self.assertLess(a, b)
        self.assertLess(b, c)
        self.assertGreater(c, a)
        self.assertEqual(a, SimpleDate(2081, 5, 24))

    def test_sorting_min_max(self):
        dates = [SimpleDate(2082, 1, 1), SimpleDate(2080, 12, 30), SimpleDate(2081, 5, 24)]
        self.assertEqual(
            [SimpleDate(2080, 12, 30), SimpleDate(2081, 5, 24), SimpleDate(2082, 1, 1)],
            sorted(dates),
        )
        self.assertEqual(SimpleDate(2080, 12, 30), min(dates))
        self.assertEqual(SimpleDate(2082, 1, 1), max(dates))


class TestClearErrors(unittest.TestCase):
    def test_total_days_bad_month(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_total_days_in_nepali_month(2081, 13)

    def test_total_days_bad_year(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_total_days_in_nepali_month(1800, 5)

    def test_month_calendar_bad_year(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_month_calendar(1800, 1)

    def test_month_calendar_bad_month(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_month_calendar(2081, 0)


class TestMemoizationParity(unittest.TestCase):
    """The cached month details must equal a fresh computation everywhere."""

    def test_cache_matches_fresh_compute(self):
        for year in (1970, 1971, 2000, 2081, 2100):
            for month in range(1, 13):
                with self.subTest(year=year, month=month):
                    cached = DateConverters.calculate_nepali_month_details(year, month)
                    fresh = DateConverters._compute_nepali_month_details(year, month)
                    self.assertEqual(fresh, cached)


if __name__ == "__main__":
    unittest.main()
