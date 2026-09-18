"""Reading a Gregorian calendar directly has to match converting a Bikram Sambat date back,
field for field, on every date the table covers."""

import unittest

from nepali_calendar_utils.calendar_model.date_converters import DateConverters
from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

ENGLISH_YEARS = range(
    NepaliCalendarDefaults.EnglishYearRange[0], NepaliCalendarDefaults.EnglishYearRange[-1] + 1
)


class TestEnglishCalendarEquivalence(unittest.TestCase):
    """There are two ways to reach a Gregorian calendar: reading the date directly, and converting
    a Bikram Sambat date back. Callers mix them, so every derived field has to agree."""

    def _assert_both_routes_agree(self, year, month, day_of_month):
        nepali = NepaliDateConverter.convert_english_to_nepali(year, month, day_of_month)
        via_round_trip = NepaliDateConverter.convert_nepali_to_english(
            nepali.year, nepali.month, nepali.day_of_month
        )
        direct = DateConverters.get_english_calendar(year, month, day_of_month)
        self.assertEqual(
            via_round_trip,
            direct,
            f"English {year}-{month}-{day_of_month} disagrees between the round trip "
            f"and the direct read",
        )

    def test_both_routes_agree_at_the_conversion_anchor(self):
        anchor = NepaliCalendarDefaults.startingEnglishCalendar
        self._assert_both_routes_agree(anchor.year, anchor.month, anchor.day_of_month)
        self._assert_both_routes_agree(anchor.year, anchor.month, anchor.day_of_month + 1)

    def test_both_routes_agree_at_the_end_of_the_convertible_range(self):
        last = NepaliCalendarDefaults.EnglishYearRange[-1]
        for month, day in ((12, 31), (12, 30), (1, 1)):
            with self.subTest(month=month, day=day):
                self._assert_both_routes_agree(last, month, day)

    def test_both_routes_agree_on_every_leap_day_in_range(self):
        for year in ENGLISH_YEARS:
            if DateConverters.get_total_days_in_english_month(year, 2) == 29:
                with self.subTest(year=year):
                    self._assert_both_routes_agree(year, 2, 29)
                    self._assert_both_routes_agree(year, 3, 1)

    def test_both_routes_agree_across_the_full_convertible_range(self):
        """Every convertible English date, both ways. This is the check that makes reading a
        Gregorian calendar directly a safe substitute for the round trip."""
        checked = 0
        for year in ENGLISH_YEARS:
            for month in range(1, 13):
                total_days = DateConverters.get_total_days_in_english_month(year, month)
                for day_of_month in range(1, total_days + 1):
                    if not DateConverters.is_english_date_in_conversion_range(
                        year, month, day_of_month
                    ):
                        continue
                    self._assert_both_routes_agree(year, month, day_of_month)
                    checked += 1
        # Every day of 1913..2043 except the 102 that precede the 1913-04-13 anchor.
        self.assertEqual(47745, checked, "Coverage of the convertible English range changed")

    def test_direct_read_rejects_a_day_the_month_does_not_have(self):
        with self.assertRaises(ValueError):
            DateConverters.get_english_calendar(2023, 2, 29)
        self.assertEqual(29, DateConverters.get_english_calendar(2024, 2, 29).day_of_month)

    def test_the_facade_exposes_the_direct_read(self):
        self.assertEqual(
            DateConverters.get_english_calendar(2024, 9, 9),
            NepaliDateConverter.get_english_calendar(2024, 9, 9),
        )
        with self.assertRaises(ValueError):
            NepaliDateConverter.get_english_calendar(2024, 5, 0)

    def test_convertibility_reports_the_dates_the_converter_accepts(self):
        anchor = NepaliCalendarDefaults.startingEnglishCalendar
        self.assertFalse(
            NepaliDateConverter.is_english_date_convertible(
                anchor.year, anchor.month, anchor.day_of_month - 1
            ),
            "The day before the anchor sits inside the year range yet cannot convert",
        )
        self.assertTrue(
            NepaliDateConverter.is_english_date_convertible(
                anchor.year, anchor.month, anchor.day_of_month
            )
        )
        self.assertFalse(NepaliDateConverter.is_english_date_convertible(anchor.year, 1, 1))
        self.assertFalse(
            NepaliDateConverter.is_english_date_convertible(
                NepaliCalendarDefaults.EnglishYearRange[-1] + 1, 1, 1
            )
        )

    def test_convertibility_agrees_with_the_converter_on_every_boundary_date(self):
        """A date the report calls convertible has to convert, and one it rejects has to raise."""
        samples = [
            (1912, 12, 31), (1913, 1, 1), (1913, 4, 12), (1913, 4, 13), (1913, 4, 14),
            (2043, 12, 31), (2044, 1, 1), (2024, 2, 29), (2024, 1, 1),
        ]
        for year, month, day in samples:
            with self.subTest(date=f"{year}-{month}-{day}"):
                convertible = NepaliDateConverter.is_english_date_convertible(year, month, day)
                try:
                    NepaliDateConverter.convert_english_to_nepali(year, month, day)
                    converted = True
                except ValueError:
                    converted = False
                self.assertEqual(convertible, converted)


if __name__ == "__main__":
    unittest.main()
