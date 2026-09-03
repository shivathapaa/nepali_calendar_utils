"""Numeral-script utilities, decoupled from language.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.data.DigitScript`` from the Kotlin
core. A :class:`DigitScript` holds the ten code points for digits 0-9 in a given
script, so any locale that shares the Devanagari digits (Nepali, Hindi, Marathi,
Maithili, Bhojpuri, Newari) can reuse the same rendering.
"""

from enum import Enum
from typing import Optional


class DigitScript(Enum):
    """Numeral script used when rendering digits in localized dates / times.

    Each member's value is the ten code points for digits 0..9 in that script.
    Use :meth:`localize` to convert Latin-digit text to the chosen script, and
    :func:`to_latin_digits` to go the other way.
    """

    #: ASCII ``0123456789``. Default for ``NepaliCalendarUtilsLang.ENGLISH``.
    LATIN = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    #: Devanagari ``०१२३४५६७८९`` (U+0966..U+096F). Default for ``NEPALI``.
    DEVANAGARI = ('०', '१', '२', '३', '४', '५', '६', '७', '८', '९')

    def localize(self, text: str) -> str:
        """Map every ASCII digit in ``text`` to this script's numeral, leaving all
        other characters untouched. :attr:`LATIN` is a no-op that returns the
        original string.
        """
        if self is DigitScript.LATIN:
            return text
        digits = self.value
        return ''.join(
            digits[ord(char) - 48] if '0' <= char <= '9' else char
            for char in text
        )


def default_digit_script(lang) -> DigitScript:
    """Default :class:`DigitScript` for a given ``NepaliCalendarUtilsLang``.

    Pass an explicit ``digit_script`` to ``NepaliDateLocale`` to override (e.g.
    show Nepali month names with Latin digits).
    """
    # Imported lazily to avoid a circular import with nepali_date_locale.
    from nepali_calendar_utils.data.nepali_date_locale import NepaliCalendarUtilsLang
    return DigitScript.DEVANAGARI if lang == NepaliCalendarUtilsLang.NEPALI else DigitScript.LATIN


def latin_digit_or_none(char: str) -> Optional[str]:
    """Reverse lookup for a single character.

    If ``char`` is a digit in any supported non-Latin script (Devanagari today),
    return the matching ASCII ``'0'..'9'``. If it is already an ASCII digit,
    return it unchanged. Otherwise return ``None``.
    """
    if '0' <= char <= '9':
        return char
    for script in DigitScript:
        if script is DigitScript.LATIN:
            continue
        try:
            idx = script.value.index(char)
        except ValueError:
            continue
        return chr(48 + idx)
    return None


def to_latin_digits(text: str) -> str:
    """Inverse of :meth:`DigitScript.localize`.

    Convert digits in any supported non-Latin script back to ASCII 0-9.
    Non-digit characters pass through unchanged.
    """
    converted = False
    out = []
    for char in text:
        latin = latin_digit_or_none(char)
        if latin is not None and latin != char:
            out.append(latin)
            converted = True
        else:
            out.append(char)
    return ''.join(out) if converted else text
