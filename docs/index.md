# nepali_calendar_utils

Utilities for working with Nepali (Bikram Sambat) dates: conversion between the Nepali
and Gregorian calendars, month details, locale-aware formatting, date arithmetic,
digit-script localization, ISO 8601 date-times, selectable-date rules, and a
calendar-event SPI with working-day helpers.

This is the pure-Python port of the `:core` module of the sibling Kotlin Multiplatform
project, [Nepali-Date-Picker](https://github.com/shivathapaa/Nepali-Date-Picker). The
conversion tables and utility semantics are kept in sync across both libraries.

## Install

Requires Python 3.11+. There are no runtime dependencies.

```bash
pip install nepali_calendar_utils
```

## Quick start

```python
from nepali_calendar_utils import NepaliDateConverter

converter = NepaliDateConverter()

converter.today_nepali_calendar          # CustomCalendar in Bikram Sambat
converter.current_time                   # SimpleTime, in Nepal time

nepali = NepaliDateConverter.convert_english_to_nepali(2024, 6, 21)
nepali.year, nepali.month, nepali.day_of_month
```

`NepaliDateConverter` is the facade for the whole library. Only the "now" readings
(`today_nepali_calendar`, `today_english_calendar`, `today_nepali_simple_date`,
`today_english_simple_date`, `current_time`) are instance properties; everything else is
a static method.

## Conventions

- **1-based indexing**: months 1..12 (1 = Baisakh / January, 12 = Chaitra / December),
  weekdays 1..7 (1 = Sunday, 7 = Saturday).
- `era`: 1 = AD, 2 = BS. `CalendarSystem` is the named form of the same value.
- The weekend is Saturday only by default, the single-day weekend Nepal observes.
- Times are always in Nepal time (`Asia/Kathmandu`, a fixed `+05:45` offset).
- Supported conversion range: BS 1970..2100, AD 1913..2043. The earliest convertible
  Gregorian date is 1913-04-13.

The [README on GitHub](https://github.com/shivathapaa/nepali_calendar_utils#readme)
carries the worked examples; the pages below are the generated API reference.

```{toctree}
:maxdepth: 2
:caption: Contents

api/index
```
