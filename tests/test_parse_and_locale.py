"""Mirrors the Kotlin core ParseAndLocaleTests."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_model import NepaliCalendarModel
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.nepali_date_locale import NameFormat, NepaliCalendarUtilsLang

C = NepaliDateConverter


class TestParse(unittest.TestCase):
    def setUp(self):
        self.model = NepaliCalendarModel()

    def test_valid_eight_char_returns_calendar(self):
        cal = self.model.parse("20810524")
        self.assertIsNotNone(cal)
        self.assertEqual((2081, 5, 24), (cal.year, cal.month, cal.day_of_month))

    def test_length_not_eight_returns_none(self):
        self.assertIsNone(self.model.parse(""))
        self.assertIsNone(self.model.parse("2081052"))
        self.assertIsNone(self.model.parse("208105244"))

    def test_non_numeric_returns_none(self):
        self.assertIsNone(self.model.parse("20XX0524"))
        self.assertIsNone(self.model.parse("abcdefgh"))

    def test_month_out_of_range_returns_none(self):
        self.assertIsNone(self.model.parse("20811324"))
        self.assertIsNone(self.model.parse("20810024"))

    def test_day_out_of_range_returns_none(self):
        self.assertIsNone(self.model.parse("20810500"))
        self.assertIsNone(self.model.parse("20810533"))

    def test_valid_range_but_invalid_day_returns_fallback(self):
        # 2081-5 has 31 days; day 32 passes the coarse 1..32 gate but is rejected by the
        # converter, so parse returns the documented stub calendar.
        cal = self.model.parse("20810532")
        self.assertIsNotNone(cal)
        self.assertEqual((2081, 5, 32, 2), (cal.year, cal.month, cal.day_of_month, cal.era))
        self.assertEqual(-1, cal.first_day_of_month)
        self.assertEqual(-1, cal.total_days_in_month)


class TestNumberLocalization(unittest.TestCase):
    def test_to_nepali_empty(self):
        self.assertEqual("", C.convert_to_nepali_number(""))

    def test_to_nepali_pure_digits(self):
        self.assertEqual("०१२३४५६७८९", C.convert_to_nepali_number("0123456789"))

    def test_to_nepali_mixed(self):
        self.assertEqual("२०२४-०६-२१", C.convert_to_nepali_number("2024-06-21"))
        self.assertEqual("v२.०.०", C.convert_to_nepali_number("v2.0.0"))

    def test_to_english_empty(self):
        self.assertEqual("", C.convert_to_english_number(""))

    def test_to_english_pure_nepali(self):
        self.assertEqual("0123456789", C.convert_to_english_number("०१२३४५६७८९"))

    def test_to_english_mixed(self):
        self.assertEqual("2024-06-21", C.convert_to_english_number("२०२४-०६-२१"))

    def test_to_english_already_english_unchanged(self):
        self.assertEqual("2024-06-21", C.convert_to_english_number("2024-06-21"))

    def test_localize_number_english_unchanged(self):
        self.assertEqual("2024", C.localize_number("2024", NepaliCalendarUtilsLang.ENGLISH))

    def test_localize_number_nepali_converted(self):
        self.assertEqual("२०२४", C.localize_number("2024", NepaliCalendarUtilsLang.NEPALI))

    def test_roundtrip_idempotent(self):
        original = "2081/05/24 09:45 AM"
        back = C.convert_to_english_number(C.convert_to_nepali_number(original))
        self.assertEqual(original, back)


class TestWeekdayNames(unittest.TestCase):
    def test_each_day_english_full(self):
        expected = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for day in range(1, 8):
            self.assertEqual(expected[day - 1],
                             C.get_weekday_name(day, NameFormat.FULL, NepaliCalendarUtilsLang.ENGLISH))

    def test_english_short_medium(self):
        self.assertEqual("S", C.get_weekday_name(1, NameFormat.SHORT))
        self.assertEqual("Sun", C.get_weekday_name(1, NameFormat.MEDIUM))

    def test_each_day_nepali_full(self):
        expected = ["आईतबार", "सोमबार", "मंगलबार", "बुधबार", "बिहिबार", "शुक्रबार", "शनिबार"]
        for day in range(1, 8):
            self.assertEqual(expected[day - 1],
                             C.get_weekday_name(day, NameFormat.FULL, NepaliCalendarUtilsLang.NEPALI))

    def test_out_of_range_throws(self):
        for bad in (0, 8, -1):
            with self.assertRaises(ValueError):
                C.get_weekday_name(bad)


class TestMonthNames(unittest.TestCase):
    def test_nepali_months_in_english(self):
        expected = ["Baisakh", "Jestha", "Asar", "Shrawn", "Bhadra", "Asoj",
                    "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"]
        for m in range(1, 13):
            self.assertEqual(expected[m - 1],
                             C.get_month_name(m, NameFormat.FULL, NepaliCalendarUtilsLang.ENGLISH))

    def test_nepali_months_in_nepali(self):
        expected = ["बैशाख", "जेठ", "असार", "साउन", "भदौ", "असोज",
                    "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत"]
        for m in range(1, 13):
            self.assertEqual(expected[m - 1],
                             C.get_month_name(m, NameFormat.FULL, NepaliCalendarUtilsLang.NEPALI))

    def test_short_format(self):
        self.assertEqual("Bai", C.get_month_name(1, NameFormat.SHORT, NepaliCalendarUtilsLang.ENGLISH))
        self.assertEqual("Chai", C.get_month_name(12, NameFormat.SHORT, NepaliCalendarUtilsLang.ENGLISH))

    def test_out_of_range_throws(self):
        for bad in (0, 13):
            with self.assertRaises(ValueError):
                C.get_month_name(bad)

    def test_english_months_in_english(self):
        expected = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
        for m in range(1, 13):
            self.assertEqual(expected[m - 1],
                             C.get_english_month_name(m, NameFormat.FULL, NepaliCalendarUtilsLang.ENGLISH))

    def test_english_months_in_nepali(self):
        expected = ["जनवरी", "फेब्रुअरी", "मार्च", "अप्रिल", "मे", "जुन",
                    "जुलाई", "अगस्ट", "सेप्टेम्बर", "अक्टोबर", "नोभेम्बर", "डिसेम्बर"]
        for m in range(1, 13):
            self.assertEqual(expected[m - 1],
                             C.get_english_month_name(m, NameFormat.FULL, NepaliCalendarUtilsLang.NEPALI))

    def test_english_month_out_of_range_throws(self):
        for bad in (0, 13):
            with self.assertRaises(ValueError):
                C.get_english_month_name(bad)


class TestReplaceDelimiter(unittest.TestCase):
    def test_empty(self):
        self.assertEqual("", C.replace_delimiter("", "-"))

    def test_no_delimiters_unchanged(self):
        self.assertEqual("hello", C.replace_delimiter("hello", "-"))

    def test_multiple_slashes(self):
        self.assertEqual("2024-06-21", C.replace_delimiter("2024/06/21", "-"))

    def test_custom_old_delimiter(self):
        self.assertEqual("a b c", C.replace_delimiter("a:b:c", " ", old_delimiter=":"))


if __name__ == "__main__":
    unittest.main()
