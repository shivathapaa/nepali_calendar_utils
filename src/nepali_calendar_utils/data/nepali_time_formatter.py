"""Parse and format :class:`SimpleTime` as the library's canonical time-of-day wire string.

Mirrors ``dev.shivathapaa.nepalidatepickerkmp.data.NepaliTimeFormatter``.

``HH:mm:ss`` with an optional nine-digit fractional part. This is the shape a ``SimpleTime``
takes on the wire everywhere the sibling Kotlin library is published, so a payload written
here reads on a Kotlin, Android, Swift or JavaScript client without any of them depending on
``kotlinx-serialization``.

Times are always read as ``Asia/Kathmandu``, the zone every ``SimpleTime`` in this library is
anchored to. No zone offset is written or accepted.

For display output (12-hour clocks, Devanagari digits, locale-aware wording) use
``NepaliDateConverter.get_formatted_time_in_english``, ``get_formatted_time_in_nepali``, or
``NepaliDateConverter.format_time_by_unicode_pattern``. This formatter is for persistence and
transport, and is fixed to Latin digits and 24-hour form on purpose.
"""

from typing import Optional

from nepali_calendar_utils.data.custom_calendar import SimpleTime

_HOUR_RANGE = range(0, 24)
_MINUTE_RANGE = range(0, 60)
_SECOND_RANGE = range(0, 60)
_NANOSECOND_RANGE = range(0, 1_000_000_000)

_CLOCK_FIELD_COUNT = 3
_CLOCK_FIELD_WIDTH = 2
_NANOSECOND_WIDTH = 9
_CLOCK_DELIMITER = ':'
_FRACTION_DELIMITER = '.'


def _decimal_int_or_none(text: str) -> Optional[int]:
    """The value of ``text`` when it is nothing but decimal digits, otherwise ``None``.

    ``int()`` alone is too permissive for a wire format: it strips surrounding whitespace and
    accepts underscore separators and a sign, so ``" 09"`` and ``"1_0"`` would parse. Guarding
    on ``str.isdecimal`` first keeps this to the digits the Kotlin side accepts, which includes
    Devanagari and other Unicode decimal digits but nothing else.
    """
    if not text.isdecimal():
        return None
    return int(text)


class NepaliTimeFormatter:
    """Formatter and parser for the canonical time-of-day wire string."""

    @staticmethod
    def format(time: SimpleTime) -> str:
        """Format ``time`` as ``HH:mm:ss``, appending ``.nnnnnnnnn`` only when
        :attr:`SimpleTime.nanosecond` is non-zero, so whole-second payloads stay compact.

        Examples: ``"09:30:00"``, ``"23:59:59.123456789"``, ``"00:00:00.000000007"``.

        No range check, pass any :class:`SimpleTime` and the result reflects it. A value outside
        the ranges :meth:`parse` accepts will not round-trip.
        """
        hour = str(time.hour).zfill(_CLOCK_FIELD_WIDTH)
        minute = str(time.minute).zfill(_CLOCK_FIELD_WIDTH)
        second = str(time.second).zfill(_CLOCK_FIELD_WIDTH)
        clock = f"{hour}{_CLOCK_DELIMITER}{minute}{_CLOCK_DELIMITER}{second}"
        if time.nanosecond == 0:
            return clock
        return f"{clock}{_FRACTION_DELIMITER}{str(time.nanosecond).zfill(_NANOSECOND_WIDTH)}"

    @staticmethod
    def parse(text: str) -> Optional[SimpleTime]:
        """Parse ``text`` as ``HH:mm:ss`` or ``HH:mm:ss.nnnnnnnnn``, returning ``None`` when it
        is not a time this formatter would have produced.

        Returns ``None`` when:

        - the clock part does not hold exactly three ``:``-separated fields,
        - any field or the fractional part is not decimal digits,
        - hour is outside ``0..23``, or minute or second is outside ``0..59``,
        - the fractional part is outside ``0..999999999``.

        The fractional part is read as a plain count of nanoseconds, so ``".7"`` means seven
        nanoseconds, not seven tenths of a second. Round-tripping through :meth:`format` returns
        the zero-padded nine-digit form.

        Field widths are not enforced, so ``"9:30:00"`` parses as ``09:30:00``. Any Unicode
        decimal digit is accepted, so Devanagari input such as ``"०९:३०:००"`` reads the same as
        its Latin form, and the two may be mixed. :meth:`format` always writes Latin digits.
        Leading and trailing whitespace is not trimmed, call ``str.strip()`` first when the input
        may carry any.
        """
        fraction_index = text.find(_FRACTION_DELIMITER)
        if fraction_index == -1:
            clock, fraction = text, "0"
        else:
            clock, fraction = text[:fraction_index], text[fraction_index + 1:]

        fields = clock.split(_CLOCK_DELIMITER)
        if len(fields) != _CLOCK_FIELD_COUNT:
            return None

        hour = _decimal_int_or_none(fields[0])
        minute = _decimal_int_or_none(fields[1])
        second = _decimal_int_or_none(fields[2])
        nanosecond = _decimal_int_or_none(fraction)
        if hour is None or minute is None or second is None or nanosecond is None:
            return None

        if hour not in _HOUR_RANGE:
            return None
        if minute not in _MINUTE_RANGE:
            return None
        if second not in _SECOND_RANGE:
            return None
        if nanosecond not in _NANOSECOND_RANGE:
            return None

        return SimpleTime(hour, minute, second, nanosecond)
