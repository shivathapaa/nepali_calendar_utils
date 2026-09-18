"""The per-year conversion anchors: their coverage, their shape, and their agreement with the
converter."""

import unittest

from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.nepali_year_month_map import english_date_map, nepali_date_map

FNV_OFFSET_BASIS = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3
MASK_64 = 0xFFFFFFFFFFFFFFFF

# Digests over every field of every pair, so any change to an anchor has to be deliberate.
EXPECTED_ENGLISH_ANCHOR_DIGEST = 18188350464217709428
EXPECTED_NEPALI_ANCHOR_DIGEST = 12015575287379078838


def _fingerprint_calendar(calendar) -> str:
    return "|".join(
        str(value)
        for value in (
            calendar.year,
            calendar.month,
            calendar.day_of_month,
            calendar.era,
            calendar.first_day_of_month,
            calendar.last_day_of_month,
            calendar.total_days_in_month,
            calendar.day_of_week_in_month,
            calendar.day_of_week,
            calendar.day_of_year,
            calendar.week_of_month,
            calendar.week_of_year,
        )
    )


def _fingerprint_map(reference_map) -> str:
    return ";".join(
        f"{year}>{_fingerprint_calendar(reference.englishDate)}"
        f">{_fingerprint_calendar(reference.nepaliDate)}"
        for year, reference in reference_map.items()
    )


def _digest(text: str) -> int:
    """FNV-1a. The arithmetic is defined the same everywhere, so the digest is a stable number."""
    value = FNV_OFFSET_BASIS
    for byte in text.encode():
        value = ((value ^ byte) * FNV_PRIME) & MASK_64
    return value


class TestAnchorTable(unittest.TestCase):
    """The per-year conversion anchors.

    Both maps hold the same English/Bikram Sambat pairs, one keyed by English year and one by
    Bikram Sambat year, and every conversion counts forward from them, so a wrong or missing entry
    shifts a whole year of dates.
    """

    def test_english_map_covers_every_year_to_the_range_end(self):
        self.assertEqual(130, len(english_date_map))
        self.assertEqual(list(range(1914, 2044)), list(english_date_map.keys()))
        for year, reference in english_date_map.items():
            self.assertEqual(year, reference.englishDate.year)

    def test_nepali_map_covers_every_year_to_the_range_end(self):
        self.assertEqual(130, len(nepali_date_map))
        self.assertEqual(list(range(1971, 2101)), list(nepali_date_map.keys()))
        for year, reference in nepali_date_map.items():
            self.assertEqual(year, reference.nepaliDate.year)

    def test_both_maps_hold_the_same_pairs_under_different_keys(self):
        for english_year, reference in english_date_map.items():
            by_nepali_year = nepali_date_map.get(reference.nepaliDate.year)
            self.assertIsNotNone(
                by_nepali_year,
                f"English anchor {english_year} has no counterpart keyed by Bikram Sambat year",
            )
            self.assertIs(
                reference,
                by_nepali_year,
                "The two anchor maps must re-key one set of pairs, not duplicate them",
            )
        self.assertEqual(len(english_date_map), len(nepali_date_map))

    def test_nepali_map_matches_its_expected_digest(self):
        fingerprint = _fingerprint_map(nepali_date_map)
        self.assertEqual(130, len(fingerprint.split(";")))
        self.assertEqual(
            EXPECTED_NEPALI_ANCHOR_DIGEST,
            _digest(fingerprint),
            "An anchor moved. test_every_anchor_pair_agrees_with_the_converter names which.",
        )

    def test_english_map_matches_its_expected_digest(self):
        fingerprint = _fingerprint_map(english_date_map)
        self.assertEqual(130, len(fingerprint.split(";")))
        self.assertEqual(
            EXPECTED_ENGLISH_ANCHOR_DIGEST,
            _digest(fingerprint),
            "An anchor moved. test_every_anchor_pair_agrees_with_the_converter names which.",
        )

    def test_every_anchor_pair_agrees_with_the_converter(self):
        """Each anchor is one year past its predecessor, so converting from the previous anchor has
        to land exactly on it. A corrupted entry survives every structural check above and fails
        here."""
        for english_year, reference in english_date_map.items():
            english = reference.englishDate
            nepali = reference.nepaliDate
            self.assertEqual(
                nepali,
                NepaliDateConverter.convert_english_to_nepali(
                    english.year, english.month, english.day_of_month
                ),
                f"Anchor {english_year}: English to Bikram Sambat disagrees with the converter",
            )
            self.assertEqual(
                english,
                NepaliDateConverter.convert_nepali_to_english(
                    nepali.year, nepali.month, nepali.day_of_month
                ),
                f"Anchor {english_year}: Bikram Sambat to English disagrees with the converter",
            )

    def test_every_anchor_is_the_first_day_of_its_nepali_year(self):
        for year, reference in nepali_date_map.items():
            self.assertEqual(1, reference.nepaliDate.month, f"Anchor {year} is not in Baisakh")
            self.assertEqual(1, reference.nepaliDate.day_of_month, f"Anchor {year} is not day 1")
            self.assertEqual(
                1, reference.nepaliDate.day_of_year, f"Anchor {year} is not day 1 of the year"
            )


if __name__ == "__main__":
    unittest.main()
