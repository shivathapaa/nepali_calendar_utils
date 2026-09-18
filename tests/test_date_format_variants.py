"""Every combination the two long-form date formatters accept: style, weekday and month name
format, language, and digit script."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.digit_script import DigitScript, default_digit_script
from nepali_calendar_utils.data.nepali_date_locale import (
    NameFormat,
    NepaliCalendarUtilsLang,
    NepaliDateFormatStyle,
    NepaliDateLocale,
)

ALL_STYLES = list(NepaliDateFormatStyle)
ALL_NAME_FORMATS = list(NameFormat)
ALL_LANGUAGES = list(NepaliCalendarUtilsLang)


class TestDateFormatVariants(unittest.TestCase):
    """Every combination the two long-form date formatters accept.

    Both share one body and differ only in which month-name list they read, which
    test_both_formatters_differ_only_in_the_month_name states directly.
    """

    # 2081-05-24 Bhadra, a Monday, is 2024-09-09 September, the same Monday.
    def setUp(self):
        self.nepali = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)

    def _locale(self, **kwargs):
        return NepaliDateLocale(**kwargs)

    def _format_nepali(self, locale):
        return NepaliDateConverter.format_nepali_date(
            self.nepali.year,
            self.nepali.month,
            self.nepali.day_of_month,
            self.nepali.day_of_week,
            locale,
        )

    def _format_english(self, locale):
        # 2024-09-09 is a Monday, day_of_week 2 in this library's Sunday-is-1 numbering.
        return NepaliDateConverter.format_english_date(2024, 9, 9, 2, locale)

    def test_every_style_bikram_sambat_english(self):
        expected = {
            NepaliDateFormatStyle.FULL: "Monday, Bhadra 24, 2081",
            NepaliDateFormatStyle.LONG: "Bhadra 24, 2081",
            NepaliDateFormatStyle.MEDIUM: "2081 Bhadra 24",
            NepaliDateFormatStyle.SHORT_MDY: "05/24/2081",
            NepaliDateFormatStyle.SHORT_YMD: "2081/05/24",
            NepaliDateFormatStyle.COMPACT_MDY: "05/24/81",
            NepaliDateFormatStyle.COMPACT_YMD: "81/05/24",
        }
        for style, value in expected.items():
            with self.subTest(style=style):
                self.assertEqual(value, self._format_nepali(self._locale(date_format=style)))

    def test_every_style_gregorian_english(self):
        expected = {
            NepaliDateFormatStyle.FULL: "Monday, September 9, 2024",
            NepaliDateFormatStyle.LONG: "September 9, 2024",
            NepaliDateFormatStyle.MEDIUM: "2024 September 9",
            NepaliDateFormatStyle.SHORT_MDY: "09/09/2024",
            NepaliDateFormatStyle.SHORT_YMD: "2024/09/09",
            NepaliDateFormatStyle.COMPACT_MDY: "09/09/24",
            NepaliDateFormatStyle.COMPACT_YMD: "24/09/09",
        }
        for style, value in expected.items():
            with self.subTest(style=style):
                self.assertEqual(value, self._format_english(self._locale(date_format=style)))

    def test_every_style_bikram_sambat_nepali(self):
        expected = {
            NepaliDateFormatStyle.FULL: "सोमबार, भदौ २४, २०८१",
            NepaliDateFormatStyle.LONG: "भदौ २४, २०८१",
            NepaliDateFormatStyle.MEDIUM: "२०८१ भदौ २४",
            NepaliDateFormatStyle.SHORT_MDY: "०५/२४/२०८१",
            NepaliDateFormatStyle.SHORT_YMD: "२०८१/०५/२४",
            NepaliDateFormatStyle.COMPACT_MDY: "०५/२४/८१",
            NepaliDateFormatStyle.COMPACT_YMD: "८१/०५/२४",
        }
        for style, value in expected.items():
            with self.subTest(style=style):
                locale = self._locale(
                    language=NepaliCalendarUtilsLang.NEPALI, date_format=style
                )
                self.assertEqual(value, self._format_nepali(locale))

    def test_weekday_name_format_only_affects_the_style_that_shows_a_weekday(self):
        full = NepaliDateFormatStyle.FULL
        self.assertEqual(
            "Monday, Bhadra 24, 2081",
            self._format_nepali(self._locale(date_format=full, week_day_name=NameFormat.FULL)),
        )
        self.assertEqual(
            "Mon, Bhadra 24, 2081",
            self._format_nepali(self._locale(date_format=full, week_day_name=NameFormat.MEDIUM)),
        )
        self.assertEqual(
            "M, Bhadra 24, 2081",
            self._format_nepali(self._locale(date_format=full, week_day_name=NameFormat.SHORT)),
        )
        for week_day_name in ALL_NAME_FORMATS:
            with self.subTest(week_day_name=week_day_name):
                self.assertEqual(
                    "Bhadra 24, 2081",
                    self._format_nepali(
                        self._locale(
                            date_format=NepaliDateFormatStyle.LONG, week_day_name=week_day_name
                        )
                    ),
                )

    def test_month_name_format_short_abbreviates_everything_else_is_full(self):
        self.assertEqual(
            "Bha 24, 2081", self._format_nepali(self._locale(month_name=NameFormat.SHORT))
        )
        self.assertEqual(
            "Bhadra 24, 2081", self._format_nepali(self._locale(month_name=NameFormat.MEDIUM))
        )
        self.assertEqual(
            "Bhadra 24, 2081", self._format_nepali(self._locale(month_name=NameFormat.FULL))
        )
        self.assertEqual(
            "Sep 9, 2024", self._format_english(self._locale(month_name=NameFormat.SHORT))
        )

    def test_both_formatters_differ_only_in_the_month_name(self):
        for language in ALL_LANGUAGES:
            for style in ALL_STYLES:
                for week_day_name in ALL_NAME_FORMATS:
                    for month_name in ALL_NAME_FORMATS:
                        with self.subTest(
                            language=language,
                            style=style,
                            week_day_name=week_day_name,
                            month_name=month_name,
                        ):
                            locale = NepaliDateLocale(
                                language=language,
                                date_format=style,
                                week_day_name=week_day_name,
                                month_name=month_name,
                            )
                            # Same numbers on both sides, so only the name list can differ.
                            bikram_sambat = NepaliDateConverter.format_nepali_date(
                                2081, 9, 9, 2, locale
                            )
                            gregorian = NepaliDateConverter.format_english_date(
                                2081, 9, 9, 2, locale
                            )
                            name_format = (
                                NameFormat.SHORT
                                if month_name == NameFormat.SHORT
                                else NameFormat.FULL
                            )
                            bikram_sambat_month = NepaliDateConverter.get_month_name(
                                9, name_format, language
                            )
                            gregorian_month = NepaliDateConverter.get_english_month_name(
                                9, name_format, language
                            )
                            self.assertEqual(
                                gregorian,
                                bikram_sambat.replace(bikram_sambat_month, gregorian_month),
                            )

    def test_explicit_latin_digits_render_nepali_month_names_with_latin_numerals(self):
        locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.LONG,
            digit_script=DigitScript.LATIN,
        )
        self.assertEqual("भदौ 24, 2081", self._format_nepali(locale))
        self.assertEqual("सेप्टेम्बर 9, 2024", self._format_english(locale))

    def test_explicit_devanagari_digits_render_english_month_names_with_devanagari_numerals(self):
        locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.ENGLISH,
            date_format=NepaliDateFormatStyle.LONG,
            digit_script=DigitScript.DEVANAGARI,
        )
        self.assertEqual("Bhadra २४, २०८१", self._format_nepali(locale))
        self.assertEqual("September ९, २०२४", self._format_english(locale))

    def test_an_explicit_script_reaches_every_numeric_field_of_every_style(self):
        expected = {
            NepaliDateFormatStyle.FULL: "सोमबार, भदौ 24, 2081",
            NepaliDateFormatStyle.LONG: "भदौ 24, 2081",
            NepaliDateFormatStyle.MEDIUM: "2081 भदौ 24",
            NepaliDateFormatStyle.SHORT_MDY: "05/24/2081",
            NepaliDateFormatStyle.SHORT_YMD: "2081/05/24",
            NepaliDateFormatStyle.COMPACT_MDY: "05/24/81",
            NepaliDateFormatStyle.COMPACT_YMD: "81/05/24",
        }
        for style, value in expected.items():
            with self.subTest(style=style):
                locale = NepaliDateLocale(
                    language=NepaliCalendarUtilsLang.NEPALI,
                    date_format=style,
                    digit_script=DigitScript.LATIN,
                )
                self.assertEqual(value, self._format_nepali(locale))

    def test_no_explicit_script_still_follows_the_language(self):
        """An unset script follows the language, which every locale built without one relies on."""
        for language in ALL_LANGUAGES:
            for style in ALL_STYLES:
                with self.subTest(language=language, style=style):
                    implicit = NepaliDateLocale(language=language, date_format=style)
                    explicit = NepaliDateLocale(
                        language=language,
                        date_format=style,
                        digit_script=default_digit_script(language),
                    )
                    self.assertEqual(
                        self._format_nepali(explicit), self._format_nepali(implicit)
                    )
                    self.assertEqual(
                        self._format_english(explicit), self._format_english(implicit)
                    )


if __name__ == "__main__":
    unittest.main()
