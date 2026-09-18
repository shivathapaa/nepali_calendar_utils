"""Ordering of a SimpleDate, and the pager position a date or a month maps to."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.data.custom_calendar import NepaliMonthCalendar, SimpleDate

YEAR_RANGE = range(
    NepaliCalendarDefaults.NepaliYearRange[0], NepaliCalendarDefaults.NepaliYearRange[-1] + 1
)
FIRST_YEAR = YEAR_RANGE.start


class TestSimpleDateOrdering(unittest.TestCase):

    def test_equal_dates_compare_equal(self):
        self.assertEqual(SimpleDate(2081, 5, 24), SimpleDate(2081, 5, 24))
        self.assertFalse(SimpleDate(2081, 5, 24) < SimpleDate(2081, 5, 24))
        self.assertFalse(SimpleDate(2081, 5, 24) > SimpleDate(2081, 5, 24))

    def test_day_orders_within_a_month(self):
        self.assertLess(SimpleDate(2081, 5, 10), SimpleDate(2081, 5, 24))
        self.assertGreater(SimpleDate(2081, 5, 24), SimpleDate(2081, 5, 10))

    def test_month_outranks_day(self):
        self.assertLess(SimpleDate(2081, 4, 32), SimpleDate(2081, 5, 1))

    def test_year_outranks_month_and_day(self):
        self.assertLess(SimpleDate(2080, 12, 30), SimpleDate(2081, 1, 1))

    def test_less_and_greater_or_equal(self):
        earlier = SimpleDate(2081, 5, 24)
        later = SimpleDate(2081, 6, 1)
        self.assertLessEqual(earlier, later)
        self.assertLessEqual(earlier, SimpleDate(2081, 5, 24))
        self.assertGreaterEqual(later, earlier)
        self.assertGreaterEqual(later, SimpleDate(2081, 6, 1))

    def test_sorts_chronologically(self):
        dates = [
            SimpleDate(2082, 1, 1),
            SimpleDate(2080, 12, 30),
            SimpleDate(2081, 5, 24),
            SimpleDate(2081, 5, 1),
        ]
        self.assertEqual(
            [
                SimpleDate(2080, 12, 30),
                SimpleDate(2081, 5, 1),
                SimpleDate(2081, 5, 24),
                SimpleDate(2082, 1, 1),
            ],
            sorted(dates),
        )

    def test_day_of_month_defaults_to_one(self):
        self.assertEqual(1, SimpleDate(2081, 5).day_of_month)


class TestIndexIn(unittest.TestCase):
    """The position a date or month holds in a pager that counts twelve months per year from the
    start of the range."""

    def test_start_of_range_is_zero(self):
        self.assertEqual(0, SimpleDate(FIRST_YEAR, 1, 1).index_in(YEAR_RANGE))

    def test_end_of_the_first_year_is_eleven(self):
        self.assertEqual(11, SimpleDate(FIRST_YEAR, 12, 30).index_in(YEAR_RANGE))

    def test_start_of_the_second_year_is_twelve(self):
        self.assertEqual(12, SimpleDate(FIRST_YEAR + 1, 1, 1).index_in(YEAR_RANGE))

    def test_arbitrary_offset(self):
        self.assertEqual(
            (2081 - FIRST_YEAR) * 12 + 4, SimpleDate(2081, 5, 24).index_in(YEAR_RANGE)
        )

    def test_a_year_below_the_range_gives_a_negative_index(self):
        self.assertLess(SimpleDate(FIRST_YEAR - 1, 1, 1).index_in(YEAR_RANGE), 0)

    def test_the_day_of_month_does_not_move_the_index(self):
        for day_of_month in (1, 15, 30):
            with self.subTest(day_of_month=day_of_month):
                self.assertEqual(
                    SimpleDate(2081, 5, 1).index_in(YEAR_RANGE),
                    SimpleDate(2081, 5, day_of_month).index_in(YEAR_RANGE),
                )

    def test_consecutive_months_give_consecutive_indices(self):
        previous = None
        for year in range(2080, 2085):
            for month in range(1, 13):
                index = SimpleDate(year, month, 1).index_in(YEAR_RANGE)
                if previous is not None:
                    self.assertEqual(previous + 1, index, f"{year}-{month} breaks the sequence")
                previous = index

    def test_month_calendar_uses_the_same_formula_as_a_date(self):
        month_calendar = NepaliMonthCalendar(
            year=2081, month=5, total_days_in_month=31, first_day_of_month=3, last_day_of_month=5
        )
        self.assertEqual(
            SimpleDate(2081, 5, 1).index_in(YEAR_RANGE), month_calendar.index_in(YEAR_RANGE)
        )

    def test_month_calendar_derives_its_leading_blank_count(self):
        month_calendar = NepaliMonthCalendar(
            year=2081, month=5, total_days_in_month=31, first_day_of_month=3, last_day_of_month=5
        )
        self.assertEqual(2, month_calendar.days_from_start_of_week_to_first_of_month)


if __name__ == "__main__":
    unittest.main()
