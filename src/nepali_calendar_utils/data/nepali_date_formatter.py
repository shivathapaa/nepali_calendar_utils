"""Parse and format :class:`SimpleDate` for short numeric text-field input.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.data.NepaliDateFormatter``.

Use this when you have a raw ``YYYY/MM/DD``-style string and need a
:class:`SimpleDate` (or vice versa). For locale-aware long-form output
("Asar 21, 2082"), use ``NepaliDateConverter.format_nepali_date(...)`` instead.

Supported patterns are limited on purpose - a free-form formatter DSL is out of
scope; the constrained surface keeps masking and validation predictable.
"""

from enum import Enum
from typing import Optional

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.data.digit_script import DigitScript, latin_digit_or_none


class DatePattern(Enum):
    """Supported text-field input/output patterns.

    Each member's value is ``(literal, delimiter, year_first)``.
    """

    #: ``YYYY/MM/DD`` - e.g. ``2082/02/14``.
    YYYY_SLASH_MM_SLASH_DD = ("YYYY/MM/DD", '/', True)

    #: ``YYYY-MM-DD`` - ISO-like, e.g. ``2082-02-14``.
    YYYY_DASH_MM_DASH_DD = ("YYYY-MM-DD", '-', True)

    #: ``DD/MM/YYYY`` - day-first, e.g. ``14/02/2082``.
    DD_SLASH_MM_SLASH_YYYY = ("DD/MM/YYYY", '/', False)

    #: ``DD-MM-YYYY`` - day-first dashed, e.g. ``14-02-2082``.
    DD_DASH_MM_DASH_YYYY = ("DD-MM-YYYY", '-', False)

    def __init__(self, literal: str, delimiter: str, year_first: bool):
        self.literal = literal
        self.delimiter = delimiter
        self.year_first = year_first

    @property
    def length(self) -> int:
        """Total visible character count when the field is full (always 10)."""
        return len(self.literal)

    @property
    def digit_count(self) -> int:
        """Number of ASCII digit characters expected (always 8)."""
        return 8


def _normalize_digits(text: str, delim1_index: int, delim2_index: int) -> Optional[str]:
    """Convert any non-Latin digits in ``text`` to Latin, only at the digit slots.

    Returns ``None`` if a slot that should hold a digit holds something else.
    Delimiter positions are passed through verbatim.
    """
    out = []
    for i, char in enumerate(text):
        if i == delim1_index or i == delim2_index:
            out.append(char)
            continue
        latin = latin_digit_or_none(char)
        if latin is None or not ('0' <= latin <= '9'):
            return None
        out.append(latin)
    return ''.join(out)


class NepaliDateFormatter:
    """Formatter/parser primitive for short numeric date strings."""

    #: Alias so callers can write ``NepaliDateFormatter.Pattern.YYYY_SLASH_MM_SLASH_DD``.
    Pattern = DatePattern

    @staticmethod
    def format(date: SimpleDate, pattern: DatePattern, script: DigitScript = DigitScript.LATIN) -> str:
        """Format ``date`` as a ``pattern.literal``-shaped string with digits in ``script``.

        No range or selectable-date checks - pass any :class:`SimpleDate`; the
        result will reflect it.
        """
        year = str(date.year).zfill(4)
        month = str(date.month).zfill(2)
        day = str(date.day_of_month).zfill(2)
        if pattern.year_first:
            raw = f"{year}{pattern.delimiter}{month}{pattern.delimiter}{day}"
        else:
            raw = f"{day}{pattern.delimiter}{month}{pattern.delimiter}{year}"
        return script.localize(raw)

    @staticmethod
    def parse(text: str, pattern: DatePattern) -> Optional[SimpleDate]:
        """Parse ``text`` as ``pattern``. Accepts Latin and Devanagari digits.

        Returns ``None`` when the length is wrong, a token is not numeric, a
        delimiter does not match, month is not in 1..12, or day is not in 1..32
        (32 is allowed because some Bikram Sambat months have 32 days; tighter
        validation against the actual month length is the caller's job).
        """
        if len(text) != pattern.length:
            return None

        delim1, delim2 = (4, 7) if pattern.year_first else (2, 5)
        normalized = _normalize_digits(text, delim1, delim2)
        if normalized is None:
            return None
        if normalized[delim1] != pattern.delimiter or normalized[delim2] != pattern.delimiter:
            return None

        if pattern.year_first:
            year_str, month_str, day_str = normalized[0:4], normalized[5:7], normalized[8:10]
        else:
            year_str, month_str, day_str = normalized[6:10], normalized[3:5], normalized[0:2]

        try:
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)
        except ValueError:
            return None

        if not (1 <= month <= 12):
            return None
        if not (1 <= day <= 32):
            return None
        return SimpleDate(year, month, day)
