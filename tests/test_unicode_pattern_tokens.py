"""Mirrors the Kotlin core UnicodePatternTokenTests."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_calendar_model import (
    DATE_FORMAT_TOKENS,
    TIME_FORMAT_TOKENS,
)
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleTime
from nepali_calendar_utils.data.nepali_date_locale import NepaliCalendarUtilsLang

ENGLISH = NepaliCalendarUtilsLang.ENGLISH


class TestUnicodePatternTokens(unittest.TestCase):
    """Token-by-token behaviour of the ``*_by_unicode_pattern`` formatters.

    The token matcher is compiled once and shared, so these pin what each token expands to, which
    token wins when one is a prefix of another, and which tokens a given entry point will replace.
    A token added to a replacement map but not to the shared matcher reaches the output untouched,
    which the sweeps at the bottom catch.
    """

    def setUp(self):
        # 2081-05-24 is a Monday, and 2024-09-09 is the same day read as Gregorian.
        self.nepali = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        self.english = NepaliDateConverter.convert_nepali_to_english(2081, 5, 24)
        self.time = SimpleTime(hour=14, minute=45, second=15, nanosecond=123456789)

    def _nepali_date(self, pattern):
        return NepaliDateConverter.format_nepali_date_by_unicode_pattern(
            pattern, self.nepali, ENGLISH
        )

    def _english_date(self, pattern):
        return NepaliDateConverter.format_english_date_by_unicode_pattern(
            pattern, self.english, ENGLISH
        )

    def _time_only(self, pattern):
        return NepaliDateConverter.format_time_by_unicode_pattern(pattern, self.time, ENGLISH)

    def _nepali_date_time(self, pattern, time="default"):
        return NepaliDateConverter.format_nepali_date_time_by_unicode_pattern(
            pattern, self.nepali, self.time if time == "default" else time, ENGLISH
        )

    def _english_date_time(self, pattern, time="default"):
        return NepaliDateConverter.format_english_date_time_by_unicode_pattern(
            pattern, self.english, self.time if time == "default" else time, ENGLISH
        )

    def test_every_date_token_expands_for_a_bikram_sambat_calendar(self):
        expected = {
            "yyyy": "2081",
            "yy": "81",
            "MMMM": "Bhadra",
            "MMM": "Bha",
            "MM": "05",
            "M": "5",
            "dd": "24",
            "d": "24",
            "D": str(self.nepali.day_of_year),
            "EEEEE": "M",
            "EEEE": "Monday",
            "E": "Mon",
            "ee": "02",
            "e": "2",
            "w": str(self.nepali.week_of_year),
        }
        for token, value in expected.items():
            with self.subTest(token=token):
                self.assertEqual(value, self._nepali_date(token))

    def test_every_time_token_expands(self):
        expected = {
            "HH": "14",
            "H": "14",
            "hh": "02",
            "h": "2",
            "mm": "45",
            "m": "45",
            "ss": "15",
            "s": "15",
            "SSSS": "1234",
            "SSS": "123",
            "SS": "12",
            "S": "1",
            "a": "pm",
            "A": "PM",
        }
        for token, value in expected.items():
            with self.subTest(token=token):
                self.assertEqual(value, self._time_only(token))

    def test_longer_token_wins_when_a_shorter_one_is_its_prefix(self):
        self.assertEqual("2081", self._nepali_date("yyyy"))
        self.assertEqual("81", self._nepali_date("yy"))
        self.assertEqual("Monday", self._nepali_date("EEEE"))
        self.assertEqual("M", self._nepali_date("EEEEE"))
        self.assertEqual("Mon", self._nepali_date("E"))
        self.assertEqual("1234", self._time_only("SSSS"))
        self.assertEqual("1", self._time_only("S"))

    def test_adjacent_tokens_each_expand_independently(self):
        self.assertEqual("20810524", self._nepali_date("yyyyMMdd"))
        self.assertEqual("2081-05-24", self._nepali_date("yyyy-MM-dd"))
        self.assertEqual("144515", self._time_only("HHmmss"))

    def test_date_only_formatter_leaves_time_tokens_alone(self):
        self.assertEqual("HH:mm", self._nepali_date("HH:mm"))
        self.assertEqual("HH:mm", self._english_date("HH:mm"))

    def test_time_only_formatter_leaves_date_tokens_alone(self):
        self.assertEqual("yyyy", self._time_only("yyyy"))
        self.assertEqual("dd", self._time_only("dd"))

    def test_date_time_formatter_with_no_time_leaves_time_tokens_alone(self):
        self.assertEqual("2081-05-24 HH:mm", self._nepali_date_time("yyyy-MM-dd HH:mm", time=None))

    def test_date_time_formatter_with_time_replaces_both_families(self):
        self.assertEqual("2081-05-24 14:45:15 PM", self._nepali_date_time("yyyy-MM-dd HH:mm:ss A"))

    def test_unsupported_characters_pass_through_unchanged(self):
        self.assertEqual("[2081] (05) {24}", self._nepali_date("[yyyy] (MM) {dd}"))
        self.assertEqual("", self._nepali_date(""))
        self.assertEqual("-- :: ++", self._time_only("-- :: ++"))

    def test_single_letter_tokens_are_replaced_inside_ordinary_words(self):
        """A pattern is matched token by token with no notion of literal text, so a single-letter
        token is replaced wherever it appears. ``s`` is seconds and ``h`` is the 12-hour token."""
        self.assertEqual("no token15 2ere", self._time_only("no tokens here"))

    def test_every_date_token_is_actually_replaced_in_every_date_entry_point(self):
        for token in DATE_FORMAT_TOKENS:
            with self.subTest(token=token):
                self.assertNotEqual(token, self._nepali_date(token))
                self.assertNotEqual(token, self._english_date(token))
                self.assertNotEqual(token, self._nepali_date_time(token))
                self.assertNotEqual(token, self._english_date_time(token))

    def test_every_time_token_is_actually_replaced_in_every_time_entry_point(self):
        for token in TIME_FORMAT_TOKENS:
            with self.subTest(token=token):
                self.assertNotEqual(token, self._time_only(token))
                self.assertNotEqual(token, self._nepali_date_time(token))
                self.assertNotEqual(token, self._english_date_time(token))

    def test_every_token_concatenated_leaves_no_token_behind(self):
        tokens = list(DATE_FORMAT_TOKENS) + list(TIME_FORMAT_TOKENS)
        formatted = self._nepali_date_time("|".join(tokens))
        parts = formatted.split("|")
        self.assertEqual(len(tokens), len(parts))
        for token, part in zip(tokens, parts):
            with self.subTest(token=token):
                self.assertTrue(part, f"Token {token} expanded to nothing")
                self.assertNotEqual(token, part)


if __name__ == "__main__":
    unittest.main()
