"""The canonical time-of-day wire string: what it writes, what it reads back, what it refuses."""

import unittest

from nepali_calendar_utils.data.custom_calendar import SimpleTime
from nepali_calendar_utils.data.nepali_time_formatter import NepaliTimeFormatter


class TestFormat(unittest.TestCase):

    def test_drops_zero_nanoseconds(self):
        self.assertEqual("09:30:00", NepaliTimeFormatter.format(SimpleTime(9, 30, 0, 0)))

    def test_includes_non_zero_nanoseconds(self):
        self.assertEqual(
            "23:59:59.123456789", NepaliTimeFormatter.format(SimpleTime(23, 59, 59, 123_456_789))
        )

    def test_pads_fraction_to_nine_digits(self):
        self.assertEqual("00:00:00.000000007", NepaliTimeFormatter.format(SimpleTime(0, 0, 0, 7)))

    def test_pads_single_digit_clock_fields(self):
        self.assertEqual("01:02:03", NepaliTimeFormatter.format(SimpleTime(1, 2, 3, 0)))


class TestParse(unittest.TestCase):

    def test_whole_seconds(self):
        self.assertEqual(SimpleTime(9, 30, 0, 0), NepaliTimeFormatter.parse("09:30:00"))

    def test_full_precision(self):
        self.assertEqual(
            SimpleTime(23, 59, 59, 123_456_789), NepaliTimeFormatter.parse("23:59:59.123456789")
        )

    def test_accepts_unpadded_clock_fields(self):
        self.assertEqual(SimpleTime(9, 5, 3, 0), NepaliTimeFormatter.parse("9:5:3"))

    def test_reads_fraction_as_a_nanosecond_count(self):
        self.assertEqual(SimpleTime(0, 0, 0, 7), NepaliTimeFormatter.parse("00:00:00.7"))

    def test_accepts_devanagari_digits(self):
        self.assertEqual(SimpleTime(9, 30, 0, 0), NepaliTimeFormatter.parse("०९:३०:००"))

    def test_accepts_mixed_digit_scripts(self):
        self.assertEqual(SimpleTime(9, 30, 0, 0), NepaliTimeFormatter.parse("०९:30:00"))

    def test_rejects_out_of_range_fields(self):
        self.assertIsNone(NepaliTimeFormatter.parse("24:00:00"))
        self.assertIsNone(NepaliTimeFormatter.parse("12:60:00"))
        self.assertIsNone(NepaliTimeFormatter.parse("12:00:60"))
        self.assertIsNone(NepaliTimeFormatter.parse("12:00:00.1000000000"))

    def test_rejects_a_wrong_field_count(self):
        self.assertIsNone(NepaliTimeFormatter.parse("12:30"))
        self.assertIsNone(NepaliTimeFormatter.parse("12:30:00:00"))

    def test_rejects_non_numeric_input(self):
        self.assertIsNone(NepaliTimeFormatter.parse("ab:30:00"))
        self.assertIsNone(NepaliTimeFormatter.parse("12:30:00."))

    def test_rejects_a_signed_field(self):
        self.assertIsNone(NepaliTimeFormatter.parse("-1:30:00"))
        self.assertIsNone(NepaliTimeFormatter.parse("+9:30:00"))

    def test_rejects_surrounding_whitespace(self):
        # int() would strip these, so the digits are checked before it is called.
        self.assertIsNone(NepaliTimeFormatter.parse(" 09:30:00"))
        self.assertIsNone(NepaliTimeFormatter.parse("09:30:00 "))

    def test_rejects_digit_separators(self):
        # int("1_0") is 10, which would let an underscore through into a wire value.
        self.assertIsNone(NepaliTimeFormatter.parse("1_0:30:00"))

    def test_rejects_non_decimal_digit_characters(self):
        self.assertIsNone(NepaliTimeFormatter.parse("²:30:00"))


class TestRoundTrip(unittest.TestCase):

    def test_every_hour_and_boundary_fraction(self):
        for hour in range(0, 24):
            for fraction in (0, 1, 7, 999_999_999):
                original = SimpleTime(hour, 59, 59, fraction)
                self.assertEqual(
                    original, NepaliTimeFormatter.parse(NepaliTimeFormatter.format(original))
                )

    def test_midnight_and_end_of_day(self):
        for time in (SimpleTime(0, 0, 0, 0), SimpleTime(23, 59, 59, 999_999_999)):
            self.assertEqual(time, NepaliTimeFormatter.parse(NepaliTimeFormatter.format(time)))


if __name__ == "__main__":
    unittest.main()
