"""Mirrors the Kotlin core CompareDatesTests, adapted to the Python compare API.

Python exposes:
  - NepaliCalendarModel().compare_dates_custom(calendar, year, month, day)
  - NepaliCalendarModel().compare_dates_simple(simple_date, year, month, day)
  - NepaliDateConverter.compare_calendar_dates(from_calendar, to_calendar)
  - NepaliDateConverter.compare_simple_dates(simple_date, year, month, day)
"""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_model import NepaliCalendarModel
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleDate

C = NepaliDateConverter


class TestModelCompareDates(unittest.TestCase):
    def setUp(self):
        self.model = NepaliCalendarModel()

    def test_simple_date_vs_tuple_same_returns_zero(self):
        self.assertEqual(0, self.model.compare_dates_simple(SimpleDate(2080, 5, 15), 2080, 5, 15))

    def test_simple_date_before_target_negative(self):
        a = SimpleDate(2080, 5, 15)
        self.assertLess(self.model.compare_dates_simple(a, 2080, 5, 16), 0)
        self.assertLess(self.model.compare_dates_simple(a, 2080, 6, 1), 0)
        self.assertLess(self.model.compare_dates_simple(a, 2081, 1, 1), 0)

    def test_simple_date_after_target_positive(self):
        a = SimpleDate(2080, 5, 15)
        self.assertGreater(self.model.compare_dates_simple(a, 2080, 5, 14), 0)
        self.assertGreater(self.model.compare_dates_simple(a, 2080, 4, 30), 0)
        self.assertGreater(self.model.compare_dates_simple(a, 2079, 12, 30), 0)

    def test_calendar_vs_tuple_same_returns_zero(self):
        cal = C.get_nepali_calendar(2081, 5, 24)
        self.assertEqual(0, self.model.compare_dates_custom(cal, 2081, 5, 24))

    def test_calendar_before_target_negative(self):
        cal = C.get_nepali_calendar(2081, 5, 24)
        self.assertLess(self.model.compare_dates_custom(cal, 2081, 5, 25), 0)
        self.assertLess(self.model.compare_dates_custom(cal, 2081, 6, 1), 0)
        self.assertLess(self.model.compare_dates_custom(cal, 2082, 1, 1), 0)

    def test_calendar_after_target_positive(self):
        cal = C.get_nepali_calendar(2081, 5, 24)
        self.assertGreater(self.model.compare_dates_custom(cal, 2081, 5, 23), 0)
        self.assertGreater(self.model.compare_dates_custom(cal, 2081, 4, 1), 0)
        self.assertGreater(self.model.compare_dates_custom(cal, 2080, 12, 30), 0)


class TestFacadeCompareDates(unittest.TestCase):
    def test_calendar_vs_calendar_same_returns_zero(self):
        cal = C.get_nepali_calendar(2081, 5, 24)
        self.assertEqual(0, C.compare_calendar_dates(cal, cal))

    def test_calendar_vs_calendar_signed_diff_by_month(self):
        earlier = C.get_nepali_calendar(2081, 3, 15)
        later = C.get_nepali_calendar(2081, 7, 15)
        self.assertLess(C.compare_calendar_dates(earlier, later), 0)
        self.assertGreater(C.compare_calendar_dates(later, earlier), 0)

    def test_calendar_vs_calendar_signed_diff_by_day_and_year(self):
        base = C.get_nepali_calendar(2081, 5, 24)
        self.assertLess(C.compare_calendar_dates(base, C.get_nepali_calendar(2081, 5, 25)), 0)
        self.assertGreater(C.compare_calendar_dates(base, C.get_nepali_calendar(2081, 5, 23)), 0)
        self.assertLess(C.compare_calendar_dates(base, C.get_nepali_calendar(2082, 5, 24)), 0)
        self.assertGreater(C.compare_calendar_dates(base, C.get_nepali_calendar(2080, 5, 24)), 0)

    def test_simple_date_overload_signed_diff(self):
        date = SimpleDate(2081, 5, 24)
        self.assertLess(C.compare_simple_dates(date, 2081, 5, 25), 0)
        self.assertGreater(C.compare_simple_dates(date, 2081, 5, 23), 0)
        self.assertLess(C.compare_simple_dates(date, 2081, 6, 1), 0)
        self.assertGreater(C.compare_simple_dates(date, 2081, 4, 30), 0)
        self.assertEqual(0, C.compare_simple_dates(date, 2081, 5, 24))

    def test_compare_agrees_with_simple_date_ordering(self):
        # Facade comparison sign must agree with SimpleDate's own ordering across a grid.
        dates = [SimpleDate(y, m, d) for y in (2080, 2081) for m in (1, 6, 12) for d in (1, 15, 28)]
        for a in dates:
            cal = C.get_nepali_calendar(a.year, a.month, a.day_of_month)
            for b in dates:
                sign_cmp = C.compare_simple_dates(a, b.year, b.month, b.day_of_month)
                sign_cal = C.compare_calendar_dates(cal, C.get_nepali_calendar(b.year, b.month, b.day_of_month))
                # Both must have the same sign as the tuple comparison.
                expected = (a > b) - (a < b)
                self.assertEqual(expected, _sign(sign_cmp), f"simple cmp {a} vs {b}")
                self.assertEqual(expected, _sign(sign_cal), f"calendar cmp {a} vs {b}")


def _sign(x):
    return (x > 0) - (x < 0)


if __name__ == "__main__":
    unittest.main()
