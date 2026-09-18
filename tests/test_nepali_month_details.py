"""Month geometry across the whole Bikram Sambat table, and the year bounds around it."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.data.nepali_year_month_map import days_in_month_map

FIRST_YEAR = NepaliCalendarDefaults.NepaliYearRange[0]
LAST_YEAR = NepaliCalendarDefaults.NepaliYearRange[-1]
SUPPORTED_YEARS = range(FIRST_YEAR, LAST_YEAR + 1)


class TestNepaliMonthDetails(unittest.TestCase):
    """The day-count table reaches one year further back than the supported range, so the year
    checks here are what stop a month lookup from answering for a year no caller can ask about."""

    def test_day_count_table_reaches_one_year_below_the_supported_range(self):
        self.assertIn(
            FIRST_YEAR - 1,
            days_in_month_map,
            "The 1969 row is what the year guards below have to exclude",
        )

    def test_month_calendar_below_supported_range_raises_despite_the_table_row(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_month_calendar(FIRST_YEAR - 1, 1)

    def test_month_calendar_above_supported_range_raises(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_month_calendar(LAST_YEAR + 1, 1)

    def test_nepali_calendar_below_supported_range_raises_despite_the_table_row(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_calendar(FIRST_YEAR - 1, 1, 1)

    def test_nepali_calendar_above_supported_range_raises(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_calendar(LAST_YEAR + 1, 1, 1)

    def test_edges_of_the_supported_range_succeed(self):
        first = NepaliDateConverter.get_nepali_month_calendar(FIRST_YEAR, 1)
        self.assertEqual(FIRST_YEAR, first.year)
        self.assertEqual(1, first.first_day_of_month)

        last = NepaliDateConverter.get_nepali_month_calendar(LAST_YEAR, 12)
        self.assertEqual(LAST_YEAR, last.year)
        self.assertEqual(12, last.month)

    def test_every_month_geometry_matches_its_own_first_and_last_day(self):
        for year in SUPPORTED_YEARS:
            for month in range(1, 13):
                month_calendar = NepaliDateConverter.get_nepali_month_calendar(year, month)
                total_days = NepaliDateConverter.get_total_days_in_nepali_month(year, month)

                self.assertEqual(
                    total_days,
                    month_calendar.total_days_in_month,
                    f"{year}-{month} total days disagree with the table",
                )
                self.assertIn(month_calendar.first_day_of_month, range(1, 8))
                self.assertIn(month_calendar.last_day_of_month, range(1, 8))

                first_day = NepaliDateConverter.get_nepali_calendar(year, month, 1)
                self.assertEqual(
                    month_calendar.first_day_of_month,
                    first_day.day_of_week,
                    f"{year}-{month} day 1 weekday disagrees with the month",
                )
                last_day = NepaliDateConverter.get_nepali_calendar(year, month, total_days)
                self.assertEqual(
                    month_calendar.last_day_of_month,
                    last_day.day_of_week,
                    f"{year}-{month} last day weekday disagrees with the month",
                )

    def test_weekday_advances_by_one_across_every_month_boundary(self):
        previous = None
        for year in SUPPORTED_YEARS:
            for month in range(1, 13):
                month_calendar = NepaliDateConverter.get_nepali_month_calendar(year, month)
                if previous is not None:
                    self.assertEqual(
                        (previous % 7) + 1,
                        month_calendar.first_day_of_month,
                        f"Weekday chain breaks entering {year}-{month}",
                    )
                previous = month_calendar.last_day_of_month

    def test_day_past_the_month_length_raises(self):
        for year in (1970, 2000, 2082, 2100):
            for month in range(1, 13):
                total_days = NepaliDateConverter.get_total_days_in_nepali_month(year, month)
                with self.assertRaises(
                    ValueError, msg=f"{year}-{month} should reject day {total_days + 1}"
                ):
                    NepaliDateConverter.get_nepali_calendar(year, month, total_days + 1)

    def test_last_day_of_every_month_is_accepted(self):
        for year in SUPPORTED_YEARS:
            for month in range(1, 13):
                total_days = NepaliDateConverter.get_total_days_in_nepali_month(year, month)
                calendar = NepaliDateConverter.get_nepali_calendar(year, month, total_days)
                self.assertEqual(total_days, calendar.day_of_month)
                self.assertEqual(total_days, calendar.total_days_in_month)

    def test_days_in_between_spans_the_whole_table_and_is_antisymmetric(self):
        start = SimpleDate(FIRST_YEAR, 1, 1)
        end = SimpleDate(
            LAST_YEAR, 12, NepaliDateConverter.get_total_days_in_nepali_month(LAST_YEAR, 12)
        )

        forward = NepaliDateConverter.get_nepali_days_in_between(start, end)
        expected = (
            sum(
                NepaliDateConverter.get_total_days_in_nepali_month(year, month)
                for year in SUPPORTED_YEARS
                for month in range(1, 13)
            )
            - 1
        )
        self.assertEqual(expected, forward)
        self.assertEqual(-forward, NepaliDateConverter.get_nepali_days_in_between(end, start))


if __name__ == "__main__":
    unittest.main()
