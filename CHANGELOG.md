# Changelog

All notable changes to `nepali_calendar_utils` are documented here.

## 3.0.0

Brings the Python package to parity with the `:core` module of the Kotlin
[Nepali-Date-Picker](https://github.com/shivathapaa/Nepali-Date-Picker) 3.1.0
release. This is an additive release - every prior public symbol works unchanged,
and all new APIs are opt-in. The major version bump aligns the package with the
Kotlin 3.x line.

The underlying Bikram Sambat data tables (day counts and reference anchors, years
1970-2100) are byte-for-byte identical to the Kotlin core, so conversions match
exactly across both libraries.

### New features

- **`DigitScript`** enum (`LATIN`, `DEVANAGARI`) that decouples numeral script
  from language, plus helpers `default_digit_script(lang)`, `to_latin_digits(s)`,
  and `latin_digit_or_none(char)`. Locales that share the Devanagari digits
  (Maithili, Newari, Hindi, Marathi, Bhojpuri) can reuse the same rendering.
  `NepaliDateConverter.localize_digits(text, script)` and `.to_latin_digits(text)`
  expose it on the facade.
- **`NepaliDateFormatter`** - a parse/format primitive for short numeric
  text-field input, with four `DatePattern`s (`YYYY/MM/DD`, `YYYY-MM-DD`,
  `DD/MM/YYYY`, `DD-MM-YYYY`). Accepts both Latin and Devanagari input.
- **`NepaliDateLocale.digit_script`** - an optional explicit numeral script,
  with a `resolved_digit_script` property. `None` (default) follows the language.
- **Holiday provider SPI** in the new `nepali_calendar_utils.holiday` package:
  `NepaliHolidayProvider`, `HolidayEntry`, `HolidayKind`, `NoOpHolidayProvider`,
  and `NepaliWeekend` (Saturday-only default). No holiday data ships by design.
  Working-day arithmetic: `working_days_between`, `next_working_day`, and
  `add_working_days` (Excel `WORKDAY` semantics), also on the converter facade.
- **`NepaliSelectableDates`** predicate plus the converter factories
  `before_date_selectable`, `after_date_selectable`, and `date_range_selectable`,
  and the wrappers `excluding_holidays` / `excluding_weekends`.
- **`SimpleDate` is now ordered** - it supports `<`, `>`, `sorted()`, `min()`,
  and `max()` (chronological by year, then month, then day).

### Correctness fixes

- `today_nepali_calendar` / `today_english_simple_date` / `today_english_calendar`
  now read the wall clock on each access. They were captured once when the model
  was constructed, so "today" never rolled over at midnight for a long-lived model.
- English dates before the earliest convertible anchor (1913-04-13) now raise
  `ValueError`. They previously passed the year-only range check and silently
  returned Nepali 1970-01-01.
- Out-of-table years now raise a clear `ValueError` instead of leaking a
  `KeyError`, and `get_total_days_in_nepali_month` validates the month range.
- `week_of_month` now uses the clamped day of month when a date is adjusted,
  matching the rest of the calculated calendar.
- `NepaliCalendarModel.parse("YYYYMMDD")` now returns a real `CustomCalendar`
  (it previously always returned an error stub because it passed a dict where a
  `SimpleDate` was expected). Logically invalid in-range dates return the
  documented stub with `era=2` and `-1` sentinel fields.
- ISO parsing of a naive datetime string (no offset, e.g. `"2011-11-04"`) now
  interprets it as Nepal local time, so `get_nepali_date_time_from_iso_format` and
  `get_english_date_nepali_time_from_iso_format` are deterministic regardless of
  the host's system time zone. They previously let `astimezone` assume the host
  zone, which gave different results on UTC hosts than on `Asia/Kathmandu` ones.

### Dependencies and portability

- **`requires-python` is now `>=3.11`.** The ISO 8601 conversion utilities rely on
  `datetime.fromisoformat` fully parsing offsets-with-seconds and `Z` suffixes,
  which landed in Python 3.11. The previous `>=3.7` floor was inaccurate (the
  package already used `zoneinfo`, which is 3.9+).
- **No third-party runtime dependencies.** Time-zone handling switched from
  `ZoneInfo("Asia/Kathmandu")` to a fixed `+05:45` offset (`datetime.timezone`).
  Nepal Standard Time has no DST or transitions in the supported range, so results
  are identical - but it no longer needs the IANA tz database, so it works on
  Windows and minimal containers where `ZoneInfo` would raise
  `ZoneInfoNotFoundError`. This mirrors the Kotlin core's `FixedOffsetTimeZone`.

### Performance

- Month-details lookups are memoized and the day offset is computed in O(1) via a
  cumulative-days prefix table, instead of re-summing every year on each call.
  Behavior-preserving.

## 2.0.1

- Corrected date of year 2082 according to Panchanga.

## 2.0.0

- Added Unicode-pattern date/time formatting and ISO 8601 conversion utilities.
