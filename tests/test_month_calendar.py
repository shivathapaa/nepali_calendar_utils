"""A calendar-tagged month: its leading blanks, its pager position, and reading one from a
Bikram Sambat month."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.calendar_system import CalendarSystem
from nepali_calendar_utils.data.custom_calendar import NepaliMonthCalendar
from nepali_calendar_utils.data.month_calendar import MonthCalendar


def _month(year: int = 2026, month: int = 9, first_day_of_month: int = 3) -> MonthCalendar:
    return MonthCalendar(
        calendar_system=CalendarSystem.GREGORIAN,
        year=year,
        month=month,
        total_days_in_month=30,
        first_day_of_month=first_day_of_month,
        last_day_of_month=4,
    )


class TestMonthCalendar(unittest.TestCase):

    def test_leading_blanks_count_back_to_sunday(self):
        self.assertEqual(0, _month(first_day_of_month=1).days_from_start_of_week_to_first_of_month)
        self.assertEqual(2, _month(first_day_of_month=3).days_from_start_of_week_to_first_of_month)
        self.assertEqual(6, _month(first_day_of_month=7).days_from_start_of_week_to_first_of_month)

    def test_index_counts_twelve_months_a_year(self):
        years = range(2020, 2031)
        self.assertEqual(0, _month(year=2020, month=1).index_in(years))
        self.assertEqual(11, _month(year=2020, month=12).index_in(years))
        self.assertEqual(12, _month(year=2021, month=1).index_in(years))
        self.assertEqual(80, _month(year=2026, month=9).index_in(years))

    def test_index_matches_the_bikram_sambat_month(self):
        # Both types page the same way, so a caller switching systems keeps its position maths.
        years = range(2080, 2091)
        nepali = NepaliMonthCalendar(
            year=2082, month=5, total_days_in_month=31, first_day_of_month=1, last_day_of_month=3
        )
        self.assertEqual(nepali.index_in(years), nepali.to_month_calendar().index_in(years))


class TestToMonthCalendar(unittest.TestCase):

    def test_tags_a_nepali_month_as_bikram_sambat(self):
        nepali = NepaliMonthCalendar(
            year=2082, month=1, total_days_in_month=31, first_day_of_month=1, last_day_of_month=3
        )
        tagged = nepali.to_month_calendar()

        self.assertIs(CalendarSystem.BIKRAM_SAMBAT, tagged.calendar_system)
        self.assertEqual(2082, tagged.year)
        self.assertEqual(1, tagged.month)
        self.assertEqual(31, tagged.total_days_in_month)
        self.assertEqual(1, tagged.first_day_of_month)
        self.assertEqual(3, tagged.last_day_of_month)

    def test_carries_the_same_leading_blanks(self):
        nepali = NepaliMonthCalendar(
            year=2082, month=6, total_days_in_month=30, first_day_of_month=5, last_day_of_month=6
        )
        self.assertEqual(
            nepali.days_from_start_of_week_to_first_of_month,
            nepali.to_month_calendar().days_from_start_of_week_to_first_of_month,
        )


class TestEnglishMonthCalendar(unittest.TestCase):

    def test_reads_a_gregorian_month(self):
        september = NepaliDateConverter.get_english_month_calendar(2026, 9)

        self.assertIs(CalendarSystem.GREGORIAN, september.calendar_system)
        self.assertEqual(2026, september.year)
        self.assertEqual(9, september.month)
        self.assertEqual(30, september.total_days_in_month)

    def test_month_lengths_follow_the_gregorian_rules(self):
        self.assertEqual(31, NepaliDateConverter.get_english_month_calendar(2026, 1).total_days_in_month)
        self.assertEqual(28, NepaliDateConverter.get_english_month_calendar(2026, 2).total_days_in_month)
        self.assertEqual(29, NepaliDateConverter.get_english_month_calendar(2024, 2).total_days_in_month)

    def test_agrees_with_the_day_by_day_read(self):
        for year, month in ((2024, 2), (2026, 9), (1913, 4), (2043, 12)):
            geometry = NepaliDateConverter.get_english_month_calendar(year, month)
            days = NepaliDateConverter.get_english_calendars_in_month(year, month)

            self.assertEqual(len(days), geometry.total_days_in_month)
            self.assertEqual(days[0].day_of_week, geometry.first_day_of_month)
            self.assertEqual(days[-1].day_of_week, geometry.last_day_of_month)


if __name__ == "__main__":
    unittest.main()
