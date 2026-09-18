"""Reading a Gregorian calendar and a Nepal-time clock out of an ISO timestamp."""

import unittest

from nepali_calendar_utils.calendar_model.date_converters import DateConverters
from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

FIRST_ENGLISH_YEAR = NepaliCalendarDefaults.EnglishYearRange[0]
LAST_ENGLISH_YEAR = NepaliCalendarDefaults.EnglishYearRange[-1]


class TestIsoEnglishCalendar(unittest.TestCase):
    """The result needs no Bikram Sambat table, so the span accepted here is wider than
    EnglishYearRange. The Bikram Sambat counterpart still needs the table and still refuses
    timestamps outside it."""

    def test_year_past_the_conversion_table_still_resolves(self):
        beyond = LAST_ENGLISH_YEAR + 7
        result = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(
            f"{beyond}-06-15T00:00:00Z"
        )
        self.assertEqual(
            (beyond, 6, 15),
            (result.custom_calendar.year, result.custom_calendar.month,
             result.custom_calendar.day_of_month),
        )
        # 00:00Z is 05:45 in Kathmandu.
        self.assertEqual((5, 45), (result.simple_time.hour, result.simple_time.minute))

    def test_year_before_the_conversion_table_still_resolves(self):
        before = FIRST_ENGLISH_YEAR - 13
        result = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(
            f"{before}-03-01T12:00:00Z"
        )
        self.assertEqual(
            (before, 3, 1),
            (result.custom_calendar.year, result.custom_calendar.month,
             result.custom_calendar.day_of_month),
        )
        self.assertEqual((17, 45), (result.simple_time.hour, result.simple_time.minute))

    def test_outside_the_table_carries_every_derived_field(self):
        beyond = LAST_ENGLISH_YEAR + 7
        from_iso = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(
            f"{beyond}-06-15T00:00:00Z"
        ).custom_calendar
        self.assertEqual(DateConverters.get_english_calendar(beyond, 6, 15), from_iso)
        self.assertIn(from_iso.day_of_week, range(1, 8))
        self.assertGreater(from_iso.week_of_year, 0)
        self.assertGreater(from_iso.day_of_year, 0)

    def test_nepali_reading_past_the_conversion_table_still_raises(self):
        beyond = LAST_ENGLISH_YEAR + 7
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_nepali_date_time_from_iso_format(f"{beyond}-06-15T00:00:00Z")

    def test_inside_the_table_matches_the_bikram_sambat_round_trip(self):
        for iso in (
            "1913-04-13T06:00:00Z",
            "2024-09-09T09:00:15Z",
            "2024-02-29T23:30:00Z",
            "2043-12-31T18:14:59Z",
        ):
            with self.subTest(iso=iso):
                english = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(
                    iso
                ).custom_calendar
                nepali = NepaliDateConverter.get_nepali_date_time_from_iso_format(
                    iso
                ).custom_calendar
                round_tripped = NepaliDateConverter.convert_nepali_to_english(
                    nepali.year, nepali.month, nepali.day_of_month
                )
                self.assertEqual(round_tripped, english)

    def test_leap_day_across_the_date_line_advances_correctly(self):
        # 2024-02-29T19:00Z is 2024-03-01T00:45 in Kathmandu.
        result = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(
            "2024-02-29T19:00:00Z"
        )
        self.assertEqual(
            (2024, 3, 1),
            (result.custom_calendar.year, result.custom_calendar.month,
             result.custom_calendar.day_of_month),
        )
        self.assertEqual((0, 45), (result.simple_time.hour, result.simple_time.minute))

    def test_invalid_string_raises(self):
        with self.assertRaises(Exception):
            NepaliDateConverter.get_english_date_nepali_time_from_iso_format("not-an-iso-date")


if __name__ == "__main__":
    unittest.main()
