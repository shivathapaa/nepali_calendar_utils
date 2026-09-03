"""Mirrors the Kotlin core DateArithmeticTests."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_model import NepaliCalendarModel
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleDate

C = NepaliDateConverter


class TestAddSubtractDays(unittest.TestCase):
    def test_add_zero_days_returns_same_calendar(self):
        self.assertEqual(C.get_nepali_calendar(2081, 5, 24),
                         C.get_nepali_calendar_after_addition_or_subtraction(2081, 5, 24, 0))

    def test_add_one_day(self):
        self.assertEqual(C.get_nepali_calendar(2081, 5, 25),
                         C.get_nepali_calendar_after_addition_or_subtraction(2081, 5, 24, 1))

    def test_subtract_one_day(self):
        self.assertEqual(C.get_nepali_calendar(2081, 5, 23),
                         C.get_nepali_calendar_after_addition_or_subtraction(2081, 5, 24, -1))

    def test_add_days_crosses_into_next_month(self):
        self.assertEqual(31, C.get_total_days_in_nepali_month(2081, 5))
        self.assertEqual(C.get_nepali_calendar(2081, 6, 4),
                         C.get_nepali_calendar_after_addition_or_subtraction(2081, 5, 25, 10))

    def test_subtract_days_crosses_into_previous_month(self):
        days_in_month4 = C.get_total_days_in_nepali_month(2081, 4)
        expected = C.get_nepali_calendar(2081, 4, 25)
        adjusted = C.get_nepali_calendar_after_addition_or_subtraction(
            2081, 5, 5, -(5 + (days_in_month4 - 25))
        )
        self.assertEqual(expected, adjusted)

    def test_add_days_crosses_year_boundary(self):
        last = C.get_total_days_in_nepali_month(2081, 12)
        self.assertEqual(C.get_nepali_calendar(2082, 1, 1),
                         C.get_nepali_calendar_after_addition_or_subtraction(2081, 12, last, 1))

    def test_subtract_days_crosses_year_boundary(self):
        last_prev = C.get_total_days_in_nepali_month(2081, 12)
        self.assertEqual(C.get_nepali_calendar(2081, 12, last_prev),
                         C.get_nepali_calendar_after_addition_or_subtraction(2082, 1, 1, -1))

    def test_add_large_positive_spanning_multiple_years(self):
        english_start = C.convert_nepali_to_english(2081, 5, 24)
        span = 1000
        adjusted = C.get_nepali_calendar_after_addition_or_subtraction(2081, 5, 24, span)
        computed_english = C.convert_nepali_to_english(adjusted.year, adjusted.month, adjusted.day_of_month)
        diff = C.get_english_days_in_between(
            SimpleDate(english_start.year, english_start.month, english_start.day_of_month),
            SimpleDate(computed_english.year, computed_english.month, computed_english.day_of_month),
        )
        self.assertEqual(span, diff)

    def test_add_days_invalid_year_throws(self):
        with self.assertRaises(ValueError):
            C.get_nepali_calendar_after_addition_or_subtraction(1900, 1, 1, 5)

    def test_add_days_invalid_month_throws(self):
        with self.assertRaises(ValueError):
            C.get_nepali_calendar_after_addition_or_subtraction(2081, 13, 1, 5)
        with self.assertRaises(ValueError):
            C.get_nepali_calendar_after_addition_or_subtraction(2081, 0, 1, 5)

    def test_add_then_subtract_is_identity(self):
        for delta in (1, 7, 31, 200, 400):
            forward = C.get_nepali_calendar_after_addition_or_subtraction(2081, 5, 24, delta)
            back = C.get_nepali_calendar_after_addition_or_subtraction(
                forward.year, forward.month, forward.day_of_month, -delta
            )
            self.assertEqual(C.get_nepali_calendar(2081, 5, 24), back, f"delta={delta}")


class TestPlusMinusMonths(unittest.TestCase):
    def setUp(self):
        self.model = NepaliCalendarModel()

    def test_plus_zero_months_returns_same_month(self):
        start = C.get_nepali_calendar(2081, 5, 1).to_nepali_month_calendar()
        self.assertEqual(start, self.model.plus_nepali_months(start, 0))

    def test_plus_thirteen_months_crosses_year(self):
        start = C.get_nepali_calendar(2081, 1, 1).to_nepali_month_calendar()
        result = self.model.plus_nepali_months(start, 13)
        self.assertEqual((2082, 2), (result.year, result.month))

    def test_minus_one_month_from_january(self):
        start = C.get_nepali_calendar(2081, 1, 1).to_nepali_month_calendar()
        result = self.model.minus_nepali_months(start, 1)
        self.assertEqual((2080, 12), (result.year, result.month))

    def test_plus_twelve_months_same_month_next_year(self):
        start = C.get_nepali_calendar(2081, 7, 1).to_nepali_month_calendar()
        result = self.model.plus_nepali_months(start, 12)
        self.assertEqual((2082, 7), (result.year, result.month))

    def test_plus_negative_equivalent_to_minus(self):
        start = C.get_nepali_calendar(2081, 5, 1).to_nepali_month_calendar()
        self.assertEqual(self.model.minus_nepali_months(start, 3),
                         self.model.plus_nepali_months(start, -3))


class TestDaysInBetween(unittest.TestCase):
    def test_same_day_returns_zero(self):
        d = SimpleDate(2081, 5, 24)
        self.assertEqual(0, C.get_nepali_days_in_between(d, d))

    def test_consecutive_days(self):
        start, end = SimpleDate(2081, 5, 24), SimpleDate(2081, 5, 25)
        self.assertEqual(1, C.get_nepali_days_in_between(start, end))
        self.assertEqual(-1, C.get_nepali_days_in_between(end, start))

    def test_across_year_boundary_matches_english(self):
        nep_start, nep_end = SimpleDate(2080, 12, 1), SimpleDate(2081, 2, 1)
        es = C.convert_nepali_to_english(nep_start.year, nep_start.month, nep_start.day_of_month)
        ee = C.convert_nepali_to_english(nep_end.year, nep_end.month, nep_end.day_of_month)
        english_diff = C.get_english_days_in_between(
            SimpleDate(es.year, es.month, es.day_of_month),
            SimpleDate(ee.year, ee.month, ee.day_of_month),
        )
        self.assertEqual(english_diff, C.get_nepali_days_in_between(nep_start, nep_end))

    def test_english_across_leap_year_includes_extra_day(self):
        self.assertEqual(366, C.get_english_days_in_between(SimpleDate(2023, 3, 1), SimpleDate(2024, 3, 1)))

    def test_invalid_start_year_throws(self):
        with self.assertRaises(ValueError):
            C.get_nepali_days_in_between(SimpleDate(1969, 1, 1), SimpleDate(2081, 1, 1))

    def test_invalid_end_year_throws(self):
        with self.assertRaises(ValueError):
            C.get_nepali_days_in_between(SimpleDate(2081, 1, 1), SimpleDate(2101, 1, 1))

    def test_swap_start_end_negates(self):
        start, end = SimpleDate(2070, 3, 15), SimpleDate(2081, 6, 12)
        forward = C.get_nepali_days_in_between(start, end)
        backward = C.get_nepali_days_in_between(end, start)
        self.assertEqual(forward, -backward)
        self.assertGreater(forward, 0)

    def test_nepali_days_between_matches_addition_offset(self):
        # get_nepali_days_in_between must agree with walking that many days forward.
        start = SimpleDate(2075, 4, 10)
        for span in (0, 1, 45, 400, 3650):
            end_cal = C.get_nepali_calendar_after_addition_or_subtraction(
                start.year, start.month, start.day_of_month, span
            )
            end = SimpleDate(end_cal.year, end_cal.month, end_cal.day_of_month)
            self.assertEqual(span, C.get_nepali_days_in_between(start, end), f"span={span}")


if __name__ == "__main__":
    unittest.main()
