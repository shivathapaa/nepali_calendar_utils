"""Reading a whole month at once.

The one-pass month reads walk the conversion table once and then advance a day at a time, so the
thing worth holding them to is that they answer exactly what converting each day on its own would.
"""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

# A spread rather than one fixture: a leap February, an ordinary month, the month carrying the
# 1913-04-13 anchor, the last convertible month, and a Bikram Sambat month that crosses the
# Gregorian new year.
ENGLISH_MONTHS = ((1913, 4), (1914, 1), (2024, 2), (2026, 9), (2043, 12))
NEPALI_MONTHS = ((1970, 1), (2081, 9), (2082, 1), (2082, 12), (2100, 12))


class TestEnglishCalendarsInMonth(unittest.TestCase):

    def test_covers_every_day_in_order(self):
        for year, month in ENGLISH_MONTHS:
            days = NepaliDateConverter.get_english_calendars_in_month(year, month)
            expected_length = NepaliDateConverter.get_total_days_in_english_month(year, month)

            self.assertEqual(expected_length, len(days))
            self.assertEqual(list(range(1, expected_length + 1)), [day.day_of_month for day in days])

    def test_matches_reading_each_day_on_its_own(self):
        for year, month in ENGLISH_MONTHS:
            days = NepaliDateConverter.get_english_calendars_in_month(year, month)
            one_by_one = [
                NepaliDateConverter.get_english_calendar(year, month, day_of_month)
                for day_of_month in range(1, len(days) + 1)
            ]
            self.assertEqual(one_by_one, days)


class TestNepaliCalendarsInEnglishMonth(unittest.TestCase):

    def test_matches_converting_each_day_on_its_own(self):
        for year, month in ENGLISH_MONTHS:
            paired = NepaliDateConverter.get_nepali_calendars_in_english_month(year, month)
            total_days = NepaliDateConverter.get_total_days_in_english_month(year, month)
            self.assertEqual(total_days, len(paired))

            for index, entry in enumerate(paired):
                day_of_month = index + 1
                convertible = NepaliDateConverter.is_english_date_convertible(year, month, day_of_month)
                if not convertible:
                    self.assertIsNone(entry, f"{year}-{month}-{day_of_month} should have no equivalent")
                    continue
                self.assertEqual(
                    NepaliDateConverter.convert_english_to_nepali(year, month, day_of_month),
                    entry,
                    f"{year}-{month}-{day_of_month} disagrees with the day-by-day conversion",
                )

    def test_the_anchor_month_is_blank_until_the_anchor(self):
        anchor = NepaliCalendarDefaults.minConvertibleEnglishDate
        paired = NepaliDateConverter.get_nepali_calendars_in_english_month(anchor.year, anchor.month)

        # Days before the anchor have no Bikram Sambat equivalent and must read as absent, not as
        # a guessed date.
        self.assertTrue(all(entry is None for entry in paired[: anchor.day_of_month - 1]))
        self.assertTrue(all(entry is not None for entry in paired[anchor.day_of_month - 1:]))

    def test_days_run_consecutively_once_they_start(self):
        for year, month in ENGLISH_MONTHS:
            present = [
                entry
                for entry in NepaliDateConverter.get_nepali_calendars_in_english_month(year, month)
                if entry is not None
            ]
            for earlier, later in zip(present, present[1:]):
                self.assertEqual(
                    1,
                    NepaliDateConverter.get_nepali_days_in_between(
                        earlier.to_simple_date(), later.to_simple_date()
                    ),
                    f"{earlier} and {later} are not consecutive",
                )


class TestEnglishCalendarsInNepaliMonth(unittest.TestCase):

    def test_matches_converting_each_day_on_its_own(self):
        for year, month in NEPALI_MONTHS:
            days = NepaliDateConverter.get_english_calendars_in_nepali_month(year, month)
            total_days = NepaliDateConverter.get_total_days_in_nepali_month(year, month)
            self.assertEqual(total_days, len(days))

            for index, entry in enumerate(days):
                day_of_month = index + 1
                converted = NepaliDateConverter.convert_nepali_to_english(year, month, day_of_month)
                self.assertEqual(
                    (converted.year, converted.month, converted.day_of_month),
                    (entry.year, entry.month, entry.day_of_month),
                    f"BS {year}-{month}-{day_of_month} disagrees with the day-by-day conversion",
                )

    def test_days_run_consecutively(self):
        for year, month in NEPALI_MONTHS:
            days = NepaliDateConverter.get_english_calendars_in_nepali_month(year, month)
            for earlier, later in zip(days, days[1:]):
                self.assertEqual(
                    1,
                    NepaliDateConverter.get_english_days_in_between(
                        earlier.to_simple_date(), later.to_simple_date()
                    ),
                    f"{earlier} and {later} are not consecutive",
                )

    def test_a_month_crossing_the_gregorian_new_year(self):
        # Poush spans December and January, so the Gregorian year changes mid-month.
        days = NepaliDateConverter.get_english_calendars_in_nepali_month(2081, 9)
        self.assertEqual({12, 1}, {day.month for day in days})
        self.assertEqual({2024, 2025}, {day.year for day in days})


if __name__ == "__main__":
    unittest.main()
