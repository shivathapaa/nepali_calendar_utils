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

### Performance

- Month-details lookups are memoized and the day offset is computed in O(1) via a
  cumulative-days prefix table, instead of re-summing every year on each call.
  Behavior-preserving.

## 2.0.1

- Corrected date of year 2082 according to Panchanga.

## 2.0.0

- Added Unicode-pattern date/time formatting and ISO 8601 conversion utilities.
