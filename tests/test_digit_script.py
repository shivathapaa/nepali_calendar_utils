import unittest

from nepali_calendar_utils.data.digit_script import (
    DigitScript,
    default_digit_script,
    latin_digit_or_none,
    to_latin_digits,
)
from nepali_calendar_utils.data.nepali_date_locale import NepaliDateLocale, NepaliCalendarUtilsLang
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter


class TestDigitScript(unittest.TestCase):
    def test_localize_latin_is_noop(self):
        self.assertEqual("2082/02/14", DigitScript.LATIN.localize("2082/02/14"))

    def test_localize_devanagari(self):
        self.assertEqual("२०८२/०२/१४", DigitScript.DEVANAGARI.localize("2082/02/14"))

    def test_localize_keeps_non_digits(self):
        self.assertEqual("Asar २१, २०८२", DigitScript.DEVANAGARI.localize("Asar 21, 2082"))

    def test_to_latin_digits_roundtrip(self):
        self.assertEqual("2082/02/14", to_latin_digits("२०८२/०२/१४"))

    def test_to_latin_digits_noop_on_latin(self):
        s = "2082-02-14"
        self.assertEqual(s, to_latin_digits(s))

    def test_latin_digit_or_none(self):
        self.assertEqual("5", latin_digit_or_none("5"))
        self.assertEqual("5", latin_digit_or_none("५"))
        self.assertIsNone(latin_digit_or_none("x"))
        self.assertIsNone(latin_digit_or_none("/"))

    def test_default_digit_script(self):
        self.assertEqual(DigitScript.LATIN, default_digit_script(NepaliCalendarUtilsLang.ENGLISH))
        self.assertEqual(DigitScript.DEVANAGARI, default_digit_script(NepaliCalendarUtilsLang.NEPALI))

    def test_locale_resolved_digit_script_follows_language(self):
        self.assertEqual(
            DigitScript.LATIN,
            NepaliDateLocale(language=NepaliCalendarUtilsLang.ENGLISH).resolved_digit_script,
        )
        self.assertEqual(
            DigitScript.DEVANAGARI,
            NepaliDateLocale(language=NepaliCalendarUtilsLang.NEPALI).resolved_digit_script,
        )

    def test_locale_resolved_digit_script_explicit_override(self):
        # Nepali month names, but Latin digits.
        locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI, digit_script=DigitScript.LATIN
        )
        self.assertEqual(DigitScript.LATIN, locale.resolved_digit_script)

    def test_converter_localize_and_to_latin(self):
        self.assertEqual("२०८२", NepaliDateConverter.localize_digits("2082", DigitScript.DEVANAGARI))
        self.assertEqual("2082", NepaliDateConverter.to_latin_digits("२०८२"))
        # Backward-compatible helpers still behave the same.
        self.assertEqual("२०८२", NepaliDateConverter.convert_to_nepali_number("2082"))
        self.assertEqual("2082", NepaliDateConverter.convert_to_english_number("२०८२"))


if __name__ == "__main__":
    unittest.main()
