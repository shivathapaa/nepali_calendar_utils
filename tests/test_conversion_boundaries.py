"""Mirrors the Kotlin core ConversionBoundaryTests, plus exhaustive round-trips."""

import unittest
from datetime import date

from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import NepaliCalendarDefaults
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter


class TestConversionBoundaries(unittest.TestCase):
    # Anchor boundary (Nepali 1970-1-1 <-> English 1913-4-13)

    def test_min_nepali_anchor_to_min_english_anchor(self):
        result = NepaliDateConverter.convert_nepali_to_english(1970, 1, 1)
        self.assertEqual((1913, 4, 13, 1), (result.year, result.month, result.day_of_month, result.era))

    def test_min_english_anchor_to_min_nepali_anchor(self):
        result = NepaliDateConverter.convert_english_to_nepali(1913, 4, 13)
        self.assertEqual((1970, 1, 1, 2), (result.year, result.month, result.day_of_month, result.era))

    def test_one_day_after_anchor_advances_english_by_one(self):
        result = NepaliDateConverter.convert_nepali_to_english(1970, 1, 2)
        self.assertEqual((1913, 4, 14), (result.year, result.month, result.day_of_month))

    # Range constants

    def test_nepali_year_range_constants(self):
        self.assertEqual(1970, NepaliCalendarDefaults.NepaliYearRange[0])
        self.assertEqual(2100, NepaliCalendarDefaults.NepaliYearRange[-1])

    def test_english_year_range_constants(self):
        self.assertEqual(1913, NepaliCalendarDefaults.EnglishYearRange[0])
        self.assertEqual(2043, NepaliCalendarDefaults.EnglishYearRange[-1])

    def test_first_day_of_week_is_sunday_one(self):
        self.assertEqual(1, NepaliCalendarDefaults.FIRST_DAY_OF_WEEK)

    # Out-of-range Nepali input throws

    def test_nepali_year_below_range_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_nepali_to_english(1969, 1, 1)

    def test_nepali_year_above_range_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_nepali_to_english(2101, 1, 1)

    def test_nepali_month_below_one_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_nepali_to_english(2080, 0, 1)

    def test_nepali_month_above_twelve_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_nepali_to_english(2080, 13, 1)

    def test_nepali_day_below_one_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_nepali_to_english(2080, 1, 0)

    def test_nepali_day_above_thirty_two_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_nepali_to_english(2080, 1, 33)

    # Out-of-range English input throws

    def test_english_year_below_range_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(1912, 12, 31)

    def test_english_year_above_range_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(2044, 1, 1)

    def test_english_month_below_one_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(2024, 0, 1)

    def test_english_month_above_twelve_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(2024, 13, 1)

    def test_english_day_below_one_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(2024, 1, 0)

    def test_english_day_above_thirty_one_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(2024, 1, 32)

    # Pre-anchor English dates rejected (the silent-wrong loophole)

    def test_before_anchor_same_year_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(1913, 1, 1)

    def test_one_day_before_anchor_throws(self):
        with self.assertRaises(ValueError):
            NepaliDateConverter.convert_english_to_nepali(1913, 4, 12)

    def test_exactly_on_anchor_succeeds(self):
        result = NepaliDateConverter.convert_english_to_nepali(1913, 4, 13)
        self.assertEqual((1970, 1, 1), (result.year, result.month, result.day_of_month))

    # Round trips at notable points

    def test_round_trip_year_start(self):
        nep = NepaliDateConverter.convert_english_to_nepali(2024, 1, 1)
        back = NepaliDateConverter.convert_nepali_to_english(nep.year, nep.month, nep.day_of_month)
        self.assertEqual((2024, 1, 1), (back.year, back.month, back.day_of_month))

    def test_round_trip_year_end(self):
        nep = NepaliDateConverter.convert_english_to_nepali(2024, 12, 31)
        back = NepaliDateConverter.convert_nepali_to_english(nep.year, nep.month, nep.day_of_month)
        self.assertEqual((2024, 12, 31), (back.year, back.month, back.day_of_month))

    def test_round_trip_leap_day(self):
        nep = NepaliDateConverter.convert_english_to_nepali(2024, 2, 29)
        back = NepaliDateConverter.convert_nepali_to_english(nep.year, nep.month, nep.day_of_month)
        self.assertEqual((2024, 2, 29), (back.year, back.month, back.day_of_month))

    def test_round_trip_nepali_year_boundary(self):
        eng = NepaliDateConverter.convert_nepali_to_english(2081, 12, 30)
        back = NepaliDateConverter.convert_english_to_nepali(eng.year, eng.month, eng.day_of_month)
        self.assertEqual((2081, 12, 30), (back.year, back.month, back.day_of_month))

    def test_max_nepali_in_range_succeeds_even_past_english_range(self):
        result = NepaliDateConverter.convert_nepali_to_english(2100, 12, 30)
        self.assertTrue(result.year > 2043)

    # Exhaustive invariants across the whole supported range

    def test_english_to_nepali_and_back_every_year(self):
        # AD -> BS -> AD identity for a representative date in every English year.
        for year in range(1914, 2044):
            for month, day in ((1, 15), (7, 20)):
                nep = NepaliDateConverter.convert_english_to_nepali(year, month, day)
                back = NepaliDateConverter.convert_nepali_to_english(nep.year, nep.month, nep.day_of_month)
                self.assertEqual(
                    (year, month, day), (back.year, back.month, back.day_of_month),
                    f"AD round-trip failed for {year}-{month}-{day}",
                )

    def test_nepali_to_english_and_back_every_year(self):
        # BS -> AD -> BS identity for New Year's Day of every Nepali year.
        for year in NepaliCalendarDefaults.NepaliYearRange:
            eng = NepaliDateConverter.convert_nepali_to_english(year, 1, 1)
            back = NepaliDateConverter.convert_english_to_nepali(eng.year, eng.month, eng.day_of_month)
            self.assertEqual((year, 1, 1), (back.year, back.month, back.day_of_month),
                             f"BS round-trip failed for {year}-1-1")

    def test_offset_engine_and_daywalk_engine_agree(self):
        # get_nepali_calendar (offset table) must fully agree with convert_english_to_nepali
        # (day-walk) for the same dates - two independent engines, exact CustomCalendar equality.
        for year in (1970, 2000, 2050, 2081, 2099):
            for month in range(1, 13):
                total = NepaliDateConverter.get_total_days_in_nepali_month(year, month)
                for day in (1, total // 2, total):
                    via_get = NepaliDateConverter.get_nepali_calendar(year, month, day)
                    eng = NepaliDateConverter.convert_nepali_to_english(year, month, day)
                    # Skip if the English intermediate falls outside the converter's
                    # supported English range (BS 2100 late months map past AD 2043).
                    if not (1913 <= eng.year <= 2043):
                        continue
                    via_walk = NepaliDateConverter.convert_english_to_nepali(
                        eng.year, eng.month, eng.day_of_month
                    )
                    self.assertEqual(via_get, via_walk, f"engine mismatch at {year}-{month}-{day}")

    def test_nepali_to_english_matches_gregorian_day_count(self):
        # The English date for BS New Year must be exactly N Gregorian days after the anchor,
        # where N is the summed BS day count - cross-checks against stdlib date arithmetic.
        anchor = date(1913, 4, 13)
        running = 0
        for year in range(1970, 2100):
            eng = NepaliDateConverter.convert_nepali_to_english(year, 1, 1)
            self.assertEqual(anchor + _timedelta_days(running),
                             date(eng.year, eng.month, eng.day_of_month),
                             f"gregorian offset mismatch at BS {year}")
            running += sum(
                NepaliDateConverter.get_total_days_in_nepali_month(year, m) for m in range(1, 13)
            )


def _timedelta_days(n):
    from datetime import timedelta
    return timedelta(days=n)


if __name__ == "__main__":
    unittest.main()
