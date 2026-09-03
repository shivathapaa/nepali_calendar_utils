import unittest

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.data.digit_script import DigitScript
from nepali_calendar_utils.data.nepali_date_formatter import NepaliDateFormatter, DatePattern


class TestNepaliDateFormatter(unittest.TestCase):
    def test_format_year_first_slash(self):
        date = SimpleDate(2082, 2, 14)
        self.assertEqual(
            "2082/02/14",
            NepaliDateFormatter.format(date, DatePattern.YYYY_SLASH_MM_SLASH_DD),
        )

    def test_format_year_first_dash(self):
        date = SimpleDate(2082, 2, 14)
        self.assertEqual(
            "2082-02-14",
            NepaliDateFormatter.format(date, DatePattern.YYYY_DASH_MM_DASH_DD),
        )

    def test_format_day_first(self):
        date = SimpleDate(2082, 2, 14)
        self.assertEqual(
            "14/02/2082",
            NepaliDateFormatter.format(date, DatePattern.DD_SLASH_MM_SLASH_YYYY),
        )
        self.assertEqual(
            "14-02-2082",
            NepaliDateFormatter.format(date, DatePattern.DD_DASH_MM_DASH_YYYY),
        )

    def test_format_pads_and_localizes(self):
        date = SimpleDate(2082, 2, 4)
        self.assertEqual(
            "२०८२/०२/०४",
            NepaliDateFormatter.format(date, DatePattern.YYYY_SLASH_MM_SLASH_DD, DigitScript.DEVANAGARI),
        )

    def test_parse_year_first(self):
        self.assertEqual(
            SimpleDate(2082, 2, 14),
            NepaliDateFormatter.parse("2082/02/14", DatePattern.YYYY_SLASH_MM_SLASH_DD),
        )

    def test_parse_day_first(self):
        self.assertEqual(
            SimpleDate(2082, 2, 14),
            NepaliDateFormatter.parse("14-02-2082", DatePattern.DD_DASH_MM_DASH_YYYY),
        )

    def test_parse_accepts_devanagari_digits(self):
        self.assertEqual(
            SimpleDate(2082, 2, 14),
            NepaliDateFormatter.parse("२०८२/०२/१४", DatePattern.YYYY_SLASH_MM_SLASH_DD),
        )

    def test_parse_wrong_length_returns_none(self):
        self.assertIsNone(NepaliDateFormatter.parse("2082/2/14", DatePattern.YYYY_SLASH_MM_SLASH_DD))

    def test_parse_wrong_delimiter_returns_none(self):
        self.assertIsNone(NepaliDateFormatter.parse("2082-02-14", DatePattern.YYYY_SLASH_MM_SLASH_DD))

    def test_parse_bad_month_returns_none(self):
        self.assertIsNone(NepaliDateFormatter.parse("2082/13/14", DatePattern.YYYY_SLASH_MM_SLASH_DD))

    def test_parse_bad_day_returns_none(self):
        self.assertIsNone(NepaliDateFormatter.parse("2082/02/33", DatePattern.YYYY_SLASH_MM_SLASH_DD))

    def test_parse_allows_day_32(self):
        self.assertEqual(
            SimpleDate(2082, 2, 32),
            NepaliDateFormatter.parse("2082/02/32", DatePattern.YYYY_SLASH_MM_SLASH_DD),
        )

    def test_parse_non_numeric_returns_none(self):
        self.assertIsNone(NepaliDateFormatter.parse("20a2/02/14", DatePattern.YYYY_SLASH_MM_SLASH_DD))

    def test_format_parse_roundtrip_all_patterns(self):
        date = SimpleDate(2081, 12, 30)
        for pattern in DatePattern:
            with self.subTest(pattern=pattern):
                formatted = NepaliDateFormatter.format(date, pattern)
                self.assertEqual(date, NepaliDateFormatter.parse(formatted, pattern))

    def test_pattern_metadata(self):
        self.assertEqual(10, DatePattern.YYYY_SLASH_MM_SLASH_DD.length)
        self.assertEqual(8, DatePattern.YYYY_SLASH_MM_SLASH_DD.digit_count)
        self.assertIs(NepaliDateFormatter.Pattern, DatePattern)


if __name__ == "__main__":
    unittest.main()
