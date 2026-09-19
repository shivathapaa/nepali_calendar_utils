# Nepali Calendar Utilities
<p align="center">
  <img src=".github/assets/images/nepali_calendar_utils_banner.png" alt="" width="100%">
</p>

A pure-Python library for working with Nepali (Bikram Sambat) dates: conversion between the Nepali
and Gregorian calendars, month details, locale-aware formatting, date arithmetic, digit-script
localization, ISO 8601 date-times, selectable-date rules, and a calendar-event SPI with working-day
arithmetic. No UI, no runtime dependencies.

<br>

<p align="center">
  <a href="https://pypi.org/project/nepali_calendar_utils/">
    <img alt="version" src="https://img.shields.io/pypi/v/nepali_calendar_utils" /></a>&nbsp;
  <a href="https://github.com/shivathapaa/nepali_calendar_utils/blob/main/LICENSE">
    <img alt="license" src="https://img.shields.io/github/license/shivathapaa/nepali_calendar_utils?labelColor=F5DDD7&color=E0BFB7"/></a>&nbsp;
  <a href="https://shivathapaa.github.io/nepali_calendar_utils/">
    <img alt="API reference" src="https://img.shields.io/badge/API%20reference-%E2%86%92-12100E?labelColor=E2E3D8"/></a>&nbsp;
  <a href="https://www.npmjs.com/package/@nepali-date-picker/web-component">
    <img alt="npm web-component" src="https://img.shields.io/badge/npm-web--component-CB3837?logo=npm&labelColor=E2E3D8"/></a>
</p>

<br>

<details>
  <summary><b>Table of contents</b></summary>

* [Installation](#installation)
* [Quick start](#quick-start)
* [Conventions and supported range](#conventions-and-supported-range)
* [Core types](#core-types)
* [Usage](#usage)
  * [Today's date and the current time](#todays-date-and-the-current-time)
  * [Date conversion](#date-conversion)
  * [Month details](#month-details)
  * [Reading a whole month at once](#reading-a-whole-month-at-once)
  * [Date arithmetic](#date-arithmetic)
  * [Comparing and sorting dates](#comparing-and-sorting-dates)
  * [Days between two dates](#days-between-two-dates)
  * [ISO 8601 date-times](#iso-8601-date-times)
  * [Formatting with a Unicode pattern](#formatting-with-a-unicode-pattern)
  * [Locale-aware formatting for display](#locale-aware-formatting-for-display)
  * [Weekday and month names](#weekday-and-month-names)
  * [Formatting a time for display](#formatting-a-time-for-display)
  * [Digit localization](#digit-localization)
  * [Short date strings with NepaliDateFormatter](#short-date-strings-with-nepalidateformatter)
  * [Times on the wire with NepaliTimeFormatter](#times-on-the-wire-with-nepalitimeformatter)
  * [Restricting selectable dates](#restricting-selectable-dates)
  * [Events, closures and working days](#events-closures-and-working-days)
* [Interoperating with Kotlin, Swift and JavaScript clients](#interoperating-with-kotlin-swift-and-javascript-clients)
* [Migrating from 3.0.0](#migrating-from-300)
* [Documentation](#documentation)
* [Other platforms and a date picker UI](#other-platforms-and-a-date-picker-ui)
* [Support](#support)
* [License](#license)
</details>

## Installation

Requires **Python 3.11+**. There are no third-party runtime dependencies: the package is pure
standard library, and Nepal time is a fixed `+05:45` offset, so no IANA time zone database is
needed.

```bash
pip install nepali_calendar_utils
```

Every public name is re-exported from the package root:

```python
from nepali_calendar_utils import *

# Or import only what you need
from nepali_calendar_utils import (
    NepaliDateConverter, CustomCalendar, SimpleDate, SimpleTime,
    NepaliDateLocale, NepaliCalendarUtilsLang, NameFormat, NepaliDateFormatStyle,
    NepaliCalendarDefaults,
)
```

The names are also importable from their defining modules
(`nepali_calendar_utils.calendar_model.nepali_date_converter` and friends) if you prefer explicit
paths.

## Quick start

```python
from nepali_calendar_utils import NepaliDateConverter, SimpleDate

converter = NepaliDateConverter()

# Today, in both calendars
converter.today_nepali_calendar     # CustomCalendar in Bikram Sambat
converter.today_english_calendar    # CustomCalendar in Gregorian

# Convert either way
nepali = NepaliDateConverter.convert_english_to_nepali(2021, 6, 21)
nepali.year, nepali.month, nepali.day_of_month   # (2078, 3, 7)

english = NepaliDateConverter.convert_nepali_to_english(2081, 3, 21)
english.year, english.month, english.day_of_month   # (2024, 7, 5)
```

`NepaliDateConverter` is the facade for everything in the library. Only the four "now" readings
(`today_nepali_calendar`, `today_english_calendar`, `today_nepali_simple_date`,
`today_english_simple_date`) and `current_time` are instance properties; every other member is a
static method you can call on the class.

## Conventions and supported range

- **1-based indexing throughout.** Months run 1..12 (1 = Baisakh / January, 12 = Chaitra /
  December). Weekdays run 1..7 (1 = Sunday, 7 = Saturday).
- **`era`**: `1` for AD (Gregorian), `2` for BS (Bikram Sambat). `CustomCalendar.calendar_system`
  is the named form of the same value.
- **Weekend** defaults to Saturday only, the single-day weekend Nepal observes
  (`NepaliWeekend.Default == frozenset({7})`).
- **Times** are always in Nepal time (`Asia/Kathmandu`, fixed `+05:45`).

Conversion is table-driven, so it is bounded. The ranges live on `NepaliCalendarDefaults`:

```python
NepaliCalendarDefaults.NepaliYearRange    # range(1970, 2101)  -> BS 1970..2100
NepaliCalendarDefaults.EnglishYearRange   # range(1913, 2044)  -> AD 1913..2043

# The English years covered by the default Nepali range, and by any sub-range of it
NepaliCalendarDefaults.GregorianYearRange              # range(1913, 2044)
NepaliCalendarDefaults.gregorian_year_range_for(range(2080, 2091))   # range(2023, 2035)
```

The two calendars start mid-year relative to each other, so a year inside `EnglishYearRange` is not
by itself enough to know a date converts:

```python
NepaliCalendarDefaults.minConvertibleEnglishDate   # SimpleDate(1913, 4, 13)
NepaliCalendarDefaults.maxConvertibleEnglishDate   # SimpleDate(2043, 12, 31)

NepaliDateConverter.is_english_date_convertible(1913, 4, 12)   # False
NepaliDateConverter.is_english_date_convertible(1913, 4, 13)   # True
```

Calls that read the Gregorian calendar alone (`get_english_calendar`,
`get_english_days_in_between`, `get_english_date_nepali_time_from_iso_format`) need no conversion
anchor, so they answer for any year. Anything that crosses between the calendars is bounded by the
ranges above.

## Core types

```python
@dataclass(frozen=True, order=True)
class SimpleDate:
    year: int
    month: int
    day_of_month: int = 1           # ordered: <, sorted(), min(), max() all work

@dataclass(frozen=True)
class SimpleTime:
    hour: int                       # 0-23
    minute: int
    second: int
    nanosecond: int

@dataclass(frozen=True)
class CustomCalendar:               # a full day in either calendar
    year: int
    month: int
    day_of_month: int
    era: int                        # 1 = AD, 2 = BS
    first_day_of_month: int
    last_day_of_month: int
    total_days_in_month: int
    day_of_week_in_month: int = -1
    day_of_week: int = -1
    day_of_year: int = -1
    week_of_month: int = -1
    week_of_year: int = -1

@dataclass(frozen=True)
class NepaliMonthCalendar:          # a Bikram Sambat month's grid geometry
    year: int
    month: int
    total_days_in_month: int
    first_day_of_month: int
    last_day_of_month: int
    days_from_start_of_week_to_first_of_month: int   # derived, leading blank cells

@dataclass(frozen=True)
class MonthCalendar:                # a month of either calendar, tagged with its system
    calendar_system: CalendarSystem
    year: int
    month: int
    total_days_in_month: int
    first_day_of_month: int
    last_day_of_month: int

@dataclass(frozen=True)
class CustomDateTime:
    custom_calendar: CustomCalendar
    simple_time: SimpleTime
```

`CalendarSystem` is the named form of `era`, so layout code does not have to care which calendar
produced a month:

```python
from nepali_calendar_utils import CalendarSystem, NepaliDateConverter

CalendarSystem.BIKRAM_SAMBAT.era        # 2
CalendarSystem.GREGORIAN.era            # 1
CalendarSystem.from_era(1)              # CalendarSystem.GREGORIAN (None for anything but 1 or 2)
CalendarSystem.BIKRAM_SAMBAT.opposite() # CalendarSystem.GREGORIAN

NepaliDateConverter.get_nepali_calendar(2082, 1, 1).calendar_system   # BIKRAM_SAMBAT
NepaliDateConverter.get_english_calendar(2024, 9, 9).calendar_system  # GREGORIAN
```

Conversion helpers move between the shapes: `CustomCalendar.to_simple_date()`,
`CustomCalendar.to_nepali_month_calendar()`, `NepaliMonthCalendar.to_month_calendar()` and
`MonthCalendar.to_nepali_month_calendar()`.

## Usage

### Today's date and the current time

```python
converter = NepaliDateConverter()

converter.today_nepali_calendar       # CustomCalendar (BS)
converter.today_english_calendar      # CustomCalendar (AD)
converter.today_nepali_simple_date    # SimpleDate (BS)
converter.today_english_simple_date   # SimpleDate (AD)
converter.current_time                # SimpleTime, in Nepal time

# The same values through the conversion helpers
converter.today_nepali_calendar.to_simple_date()             # SimpleDate
converter.today_english_calendar.to_nepali_month_calendar()  # NepaliMonthCalendar
```

### Date conversion

```python
NepaliDateConverter.convert_english_to_nepali(2021, 6, 21)   # CustomCalendar(2078, 3, 7, era=2, ...)
NepaliDateConverter.convert_nepali_to_english(2081, 3, 21)   # CustomCalendar(2024, 7, 5, era=1, ...)

# Full details for a Bikram Sambat date, without converting
NepaliDateConverter.get_nepali_calendar(2082, 4, 16)         # CustomCalendar(..., day_of_week=6, ...)

# Full details for a Gregorian date, read directly. Needs no conversion anchor, so it
# answers for any year, not only those the conversion table covers.
NepaliDateConverter.get_english_calendar(2024, 9, 9)         # CustomCalendar(era=1, ...)
```

### Month details

```python
NepaliDateConverter.get_total_days_in_nepali_month(2081, 10)    # 30
NepaliDateConverter.get_total_days_in_english_month(2024, 2)    # 29

asar_2078 = NepaliDateConverter.get_nepali_month_calendar(2078, 3)
# NepaliMonthCalendar(year=2078, month=3, total_days_in_month=31,
#                     first_day_of_month=3, last_day_of_month=5,
#                     days_from_start_of_week_to_first_of_month=2)

# The Gregorian counterpart, tagged with the system it belongs to
september_2026 = NepaliDateConverter.get_english_month_calendar(2026, 9)   # MonthCalendar
september_2026.calendar_system                              # CalendarSystem.GREGORIAN
september_2026.days_from_start_of_week_to_first_of_month    # 2, the leading blank cells before day 1

# Moving between the two shapes. to_nepali_month_calendar copies the year and month verbatim,
# so narrowing a Gregorian month yields a NepaliMonthCalendar holding Gregorian numbers.
asar_2078.to_month_calendar().to_nepali_month_calendar() == asar_2078    # True
```

### Reading a whole month at once

```python
# Every day of a Gregorian month, in day order
NepaliDateConverter.get_english_calendars_in_month(2026, 9)     # list[CustomCalendar], 30 entries

# The Bikram Sambat equivalent of every day of a Gregorian month. A day before the conversion
# anchor (AD 1913-04-13) has no equivalent and comes back as None rather than a guess.
paired = NepaliDateConverter.get_nepali_calendars_in_english_month(2026, 9)
convertible = [day for day in paired if day is not None]

# The mirror: every day of a Bikram Sambat month as a Gregorian calendar
NepaliDateConverter.get_english_calendars_in_nepali_month(2082, 1)   # list[CustomCalendar], 31 entries
```

Each of these converts the whole month in one pass, so prefer them over calling
`convert_english_to_nepali` or `convert_nepali_to_english` in a loop.

### Date arithmetic

Adds or subtracts days from a Bikram Sambat date, rolling over month and year boundaries.

```python
# Add 10 days to 2081-03-15
NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 3, 15, 10)
# CustomCalendar(year=2081, month=3, day_of_month=25, ...)

# Subtract 5 days from 2081-03-15
NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 3, 15, -5)
# CustomCalendar(year=2081, month=3, day_of_month=10, ...)

# Add 50 days, crossing into the next year
NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 11, 15, 50)
# CustomCalendar(year=2082, month=1, day_of_month=5, ...)
```

### Comparing and sorting dates

Both comparison helpers return a negative number when the first date is earlier, zero when the two
are equal, and a positive number when the first date is later.

```python
today = NepaliDateConverter().today_nepali_calendar

NepaliDateConverter.compare_simple_dates(today.to_simple_date(), 2090, 2, 12)   # negative
NepaliDateConverter.compare_calendar_dates(today, today)                       # 0
```

`SimpleDate` is ordered, so the Python operators work directly:

```python
from nepali_calendar_utils import SimpleDate

SimpleDate(2081, 5, 24) < SimpleDate(2081, 5, 25)   # True

dates = [SimpleDate(2082, 1, 1), SimpleDate(2080, 12, 30), SimpleDate(2081, 5, 24)]
sorted(dates)       # [2080-12-30, 2081-05-24, 2082-01-01]
min(dates), max(dates)
```

### Days between two dates

The end date is excluded from the count; add 1 to include it.

```python
NepaliDateConverter.get_nepali_days_in_between(SimpleDate(1998, 11, 23), SimpleDate(2098, 4, 21))
# 36313

NepaliDateConverter.get_english_days_in_between(SimpleDate(2009, 6, 21), SimpleDate(2500, 3, 23))
# 179244
```

`get_nepali_days_in_between` raises `ValueError` when either year is outside `NepaliYearRange`.
`get_english_days_in_between` works on Gregorian dates alone, so it is not bounded by the table.

### ISO 8601 date-times

The `SimpleTime` you pass in is read as Nepal time and written out in UTC, which is what makes the
result safe to store or hand to another time zone.

```python
converter = NepaliDateConverter()
time = SimpleTime(14, 30, 15, 28900000)

NepaliDateConverter.format_english_date_nepali_time_to_iso(SimpleDate(2025, 1, 25), time)
# "2025-01-25T08:45:15.028900Z"

NepaliDateConverter.format_nepali_datetime_to_iso(SimpleDate(2081, 10, 12), time)
# "2025-01-25T08:45:15.028900Z"
```

The fractional part is written only when the nanosecond is non-zero. `simple_time` is optional and
defaults to the current time.

Reading back gives a `CustomDateTime`, a `CustomCalendar` plus the `SimpleTime` in Nepal time:

```python
NepaliDateConverter.get_nepali_date_time_from_iso_format("2024-09-09T09:00:15Z")
# CustomDateTime(custom_calendar=CustomCalendar(year=2081, month=5, day_of_month=24, era=2, ...),
#                simple_time=SimpleTime(hour=14, minute=45, second=15, nanosecond=0))

NepaliDateConverter.get_english_date_nepali_time_from_iso_format("2024-09-09T09:00:15Z")
# CustomDateTime(custom_calendar=CustomCalendar(year=2024, month=9, day_of_month=9, era=1, ...),
#                simple_time=SimpleTime(hour=14, minute=45, second=15, nanosecond=0))
```

Both accept the usual ISO 8601 shapes: `"2020-08-30T18:43:00Z"`, `"2020-08-30T18:43:00.503Z"`,
`"2020-08-30T18:40:00+03:00"`, `"2011-11-04"`, `"2011-11-04 00:05:23.283"`, and so on. An
unparseable string raises `ValueError`.

### Formatting with a Unicode pattern

```python
converter = NepaliDateConverter()
time = SimpleTime(14, 45, 15, 0)

# Time only
NepaliDateConverter.format_time_by_unicode_pattern(
    unicode_pattern="hh:mm:ss a", time=time, language=NepaliCalendarUtilsLang.NEPALI
)   # "०२:४५:१५ दिउँसो"

NepaliDateConverter.format_time_by_unicode_pattern(
    unicode_pattern="hh:mm:ss A", time=time, language=NepaliCalendarUtilsLang.ENGLISH
)   # "02:45:15 PM"

# Nepali date only
nepali_calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)

NepaliDateConverter.format_nepali_date_by_unicode_pattern(
    unicode_pattern="EEEE, MMMM dd yyyy",
    calendar=nepali_calendar,
    language=NepaliCalendarUtilsLang.NEPALI,   # use ENGLISH for English output
)   # "सोमबार, भदौ २४ २०८१"

# English date only
english_calendar = NepaliDateConverter.get_english_calendar(2025, 5, 24)

NepaliDateConverter.format_english_date_by_unicode_pattern(
    unicode_pattern="E, MMM dd yyyy",
    calendar=english_calendar,
    language=NepaliCalendarUtilsLang.ENGLISH,  # use NEPALI for Nepali output
)   # "Sat, May 24 2025"

# Date and time together
NepaliDateConverter.format_nepali_date_time_by_unicode_pattern(
    unicode_pattern="yyyy MMMM dd, EEEE a hh:mm:ss",
    calendar=nepali_calendar,
    time=time,
    language=NepaliCalendarUtilsLang.NEPALI,
)   # "२०८१ भदौ २४, सोमबार दिउँसो ०२:४५:१५"

NepaliDateConverter.format_english_date_time_by_unicode_pattern(
    unicode_pattern="yyyy MMMM dd, EEEE hh:mm:ss A",
    calendar=NepaliDateConverter.get_english_calendar(2025, 5, 26),
    time=time,
    language=NepaliCalendarUtilsLang.ENGLISH,
)   # "2025 May 26, Monday 02:45:15 PM"
```

`time` is optional on the date-time functions; omit it to format the date alone.

Supported placeholders:

| Field | Tokens |
| --- | --- |
| Year | `yyyy` (2025), `yy` (25) |
| Month | `MMMM` (full name), `MMM` (short name), `MM` (01), `M` (1) |
| Day | `dd` (04), `d` (4), `D` (day of year, 1-366) |
| Week | `w` (week of year) |
| Weekday | `EEEE` (full), `E` (medium), `EEEEE` (shortest), `ee` (02), `e` (2) |
| Hour | `HH` / `H` (24-hour), `hh` / `h` (12-hour) |
| Minute, second | `mm` / `m`, `ss` / `s` |
| Fractional second | `SSSS`, `SSS`, `SS`, `S` |
| Period | `A` (`PM`), `a` (`pm`). Both render the localized period in Nepali (`दिउँसो`) |

Month and weekday names follow `language`; so do the digits, which render in Devanagari for
`NEPALI` and Latin for `ENGLISH`.

### Locale-aware formatting for display

`NepaliDateLocale` controls the language, the date style, and how weekday and month names are
abbreviated. Set `digit_script` to render digits in a script other than the language's default.

```python
converter = NepaliDateConverter()
today_nepali = converter.today_nepali_calendar
today_english = converter.today_english_calendar

full_nepali = NepaliDateLocale(
    language=NepaliCalendarUtilsLang.NEPALI,
    date_format=NepaliDateFormatStyle.FULL,
    week_day_name=NameFormat.FULL,
    month_name=NameFormat.FULL,
)

# For a calendar read on 2081-10-12 (a Saturday):
NepaliDateConverter.format_nepali_date_from_calendar(today_nepali, full_nepali)
# "शनिबार, माघ १२, २०८१"
NepaliDateConverter.format_nepali_date_from_calendar(today_nepali, NepaliDateLocale())
# "Magh 12, 2081"
NepaliDateConverter.format_nepali_date_from_calendar(today_nepali, NepaliCalendarDefaults.DefaultLocale)
# "Magh 12, 2081"

# Without a calendar object, so without date validation: you supply the day of the week
NepaliDateConverter.format_nepali_date(2081, 3, 21, 5, NepaliCalendarDefaults.DefaultLocale)
# "Asar 21, 2081"

# The English calendar, same locale rules. For 2025-01-25 (a Saturday):
NepaliDateConverter.format_english_date_from_calendar(today_english, NepaliDateLocale())
# "January 25, 2025"
NepaliDateConverter.format_english_date(2025, 1, 25, 7, full_nepali)
# "शनिबार, जनवरी २५, २०२५"
```

`NepaliDateFormatStyle` offers `FULL`, `LONG` (the default), `MEDIUM`, `SHORT_MDY`, `SHORT_YMD`,
`COMPACT_MDY` and `COMPACT_YMD`.

### Weekday and month names

```python
NepaliDateConverter.get_weekday_name(2, NameFormat.FULL, NepaliCalendarUtilsLang.NEPALI)     # "सोमबार"
NepaliDateConverter.get_weekday_name(5, NameFormat.MEDIUM, NepaliCalendarUtilsLang.ENGLISH)  # "Thu"

NepaliDateConverter.get_month_name(12, NameFormat.FULL, NepaliCalendarUtilsLang.NEPALI)      # "चैत"
NepaliDateConverter.get_month_name(3, NameFormat.SHORT, NepaliCalendarUtilsLang.ENGLISH)     # "Asa"

NepaliDateConverter.get_english_month_name(6, NameFormat.FULL, NepaliCalendarUtilsLang.NEPALI)  # "जुन"
```

`get_month_name` names Bikram Sambat months; `get_english_month_name` names Gregorian ones. Both
raise `ValueError` outside 1..12, as `get_weekday_name` does outside 1..7.

### Formatting a time for display

```python
time = SimpleTime(0, 4, 0, 0)

NepaliDateConverter.get_formatted_time_in_nepali(simple_time=time, use_12_hour_format=True)
# "राति १२ : ०४"
NepaliDateConverter.get_formatted_time_in_english(simple_time=time, use_12_hour_format=False)
# "0:04"
```

### Digit localization

`DigitScript` holds the ten code points for digits 0-9 in a script, decoupled from language, so any
locale sharing the Devanagari digits can reuse it.

```python
from nepali_calendar_utils import (
    NepaliDateConverter, DigitScript, NepaliDateLocale, NepaliCalendarUtilsLang,
)

NepaliDateConverter.localize_digits("2082/02/14", DigitScript.DEVANAGARI)   # "२०८२/०२/१४"
NepaliDateConverter.to_latin_digits("२०८२/०२/१४")                            # "2082/02/14"

# Render Nepali month names with Latin digits
locale = NepaliDateLocale(language=NepaliCalendarUtilsLang.NEPALI, digit_script=DigitScript.LATIN)
locale.resolved_digit_script    # DigitScript.LATIN; left as None it follows the language
```

The older string helpers remain, and work on whole strings, leaving non-digits untouched:

```python
NepaliDateConverter.convert_to_nepali_number("Today is 2024")     # "Today is २०२४"
NepaliDateConverter.convert_to_english_number("२०२४ सोमबार")       # "2024 सोमबार"

# localize_number renders Latin digits in the language's script. It is a no-op for ENGLISH,
# since Latin is already the English script; use convert_to_english_number to go the other way.
NepaliDateConverter.localize_number("Today is 2024", NepaliCalendarUtilsLang.NEPALI)   # "Today is २०२४"
```

`replace_delimiter` swaps separators in an already-formatted string. With no `old_delimiter`, every
non-alphanumeric character is replaced:

```python
NepaliDateConverter.replace_delimiter("2024/06/21", "-")        # "2024-06-21"
NepaliDateConverter.replace_delimiter("२०२४/०६/२१", "-")         # "२०२४-०६-२१"
NepaliDateConverter.replace_delimiter("09:45 AM", " ", ":")     # "09 45 AM"
```

### Short date strings with `NepaliDateFormatter`

For text-field input and simple numeric output. `DatePattern` offers `YYYY_SLASH_MM_SLASH_DD`,
`YYYY_DASH_MM_DASH_DD`, `DD_SLASH_MM_SLASH_YYYY` and `DD_DASH_MM_DASH_YYYY`.

```python
from nepali_calendar_utils import NepaliDateFormatter, DatePattern, DigitScript, SimpleDate

NepaliDateFormatter.format(SimpleDate(2082, 2, 14), DatePattern.YYYY_SLASH_MM_SLASH_DD)
# "2082/02/14"
NepaliDateFormatter.format(SimpleDate(2082, 2, 14), DatePattern.DD_DASH_MM_DASH_YYYY, DigitScript.DEVANAGARI)
# "१४-०२-२०८२"

# Parsing accepts Latin and Devanagari digits, and returns None on anything invalid
NepaliDateFormatter.parse("2082/02/14", DatePattern.YYYY_SLASH_MM_SLASH_DD)   # SimpleDate(2082, 2, 14)
NepaliDateFormatter.parse("२०८२/०२/१४", DatePattern.YYYY_SLASH_MM_SLASH_DD)   # SimpleDate(2082, 2, 14)
NepaliDateFormatter.parse("2082/13/14", DatePattern.YYYY_SLASH_MM_SLASH_DD)   # None, bad month
```

`parse` checks shape only: month must be 1..12 and day 1..32, since some Bikram Sambat months have
32 days. Validating the day against the actual month length is the caller's job. For long-form,
locale-aware output use `format_nepali_date_from_calendar` instead.

### Times on the wire with `NepaliTimeFormatter`

The transport form of a `SimpleTime`: `HH:mm:ss`, fixed to Latin digits and a 24-hour clock, with a
nine-digit fractional part appended only when the nanosecond is non-zero.

```python
from nepali_calendar_utils import NepaliTimeFormatter, SimpleTime

NepaliTimeFormatter.format(SimpleTime(9, 30, 0, 0))             # "09:30:00"
NepaliTimeFormatter.format(SimpleTime(23, 59, 59, 123456789))   # "23:59:59.123456789"

# Parsing accepts Latin and Devanagari digits, and returns None on anything it would not have written
NepaliTimeFormatter.parse("09:30:00")    # SimpleTime(9, 30, 0, 0)
NepaliTimeFormatter.parse("9:5:3")       # SimpleTime(9, 5, 3, 0), field widths are not enforced
NepaliTimeFormatter.parse("०९:३०:००")     # SimpleTime(9, 30, 0, 0)
NepaliTimeFormatter.parse("24:00:00")    # None, hour out of range
```

The fractional part is a plain count of nanoseconds, so `".7"` means seven nanoseconds. For
something shown to a user, reach for `get_formatted_time_in_english`,
`get_formatted_time_in_nepali` or `format_time_by_unicode_pattern` instead.

### Restricting selectable dates

`NepaliSelectableDates` is a predicate pair: one test for a date, one for a year. The factories live
on `NepaliDateConverter`.

```python
from nepali_calendar_utils import NepaliDateConverter, SimpleDate

before = NepaliDateConverter.before_date_selectable(SimpleDate(2081, 5, 24))
after = NepaliDateConverter.after_date_selectable(SimpleDate(2081, 5, 24), include_date=True)
in_range = NepaliDateConverter.date_range_selectable(SimpleDate(2081, 1, 1), SimpleDate(2081, 12, 30))

calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 23)
before.is_selectable_date(calendar)    # True
before.is_selectable_year(2082)        # False
```

Both bounds are exclusive by default; pass `include_date=True` (or `include_min_date` /
`include_max_date` on `date_range_selectable`) to include them. Subclass `NepaliSelectableDates` for
any rule the factories do not cover.

### Events, closures and working days

A holiday is one kind of calendar event, alongside festivals, school programmes, deadlines and
birthdays. What separates a closure from an ordinary day is the `closes_offices` flag on the event,
not its category.

**No event data ships with this library by design.** Nepali holiday lists change year to year and
every institution keeps its own, so you supply a `NepaliEventProvider`.

```python
from nepali_calendar_utils import (
    SimpleDate, NepaliEventProvider, NepaliCalendarEvent, NepaliEventKind,
    NepaliCalendarPolicy, NepaliSelectableDates,
    working_days_between, next_working_day, add_working_days,
    excluding_weekends, excluding_closures,
)

class MyEvents(NepaliEventProvider):
    _by_year = {
        2082: {
            NepaliCalendarEvent(SimpleDate(2082, 1, 1), "नयाँ वर्ष",
                                NepaliEventKind.GOVERNMENT_PUBLIC),
        },
    }

    def events(self, year):
        return self._by_year.get(year, set())

provider = MyEvents()
```

`NepaliEventKind` is deliberately narrow: `GOVERNMENT_PUBLIC`, `RELIGIOUS`, `REGIONAL` and
`OBSERVANCE`. `closes_offices` defaults to what the kind usually means (an `OBSERVANCE` does not
close, the other three do) and can be overridden per event. `id` and `payload` are carried through
untouched for an app to correlate a day back to its own record.

Providers compose:

```python
combined = national_list + my_own_list          # everything either side reports
public_only = combined.filtered(lambda event: event.kind is NepaliEventKind.GOVERNMENT_PUBLIC)
```

Use `NoOpEventProvider` when you want the event-aware APIs but have not wired a data source yet.

**Working-day arithmetic** follows Excel `WORKDAY` semantics. The weekend defaults to Saturday
only; pass your own set of day-of-week numbers to override.

```python
working_days_between(SimpleDate(2082, 1, 1), SimpleDate(2082, 1, 15), provider)   # 11
next_working_day(SimpleDate(2082, 1, 1), provider)                                # SimpleDate(2082, 1, 2)
add_working_days(SimpleDate(2082, 1, 1), 5, provider)                             # SimpleDate(2082, 1, 7)

# A Friday-and-Saturday weekend
add_working_days(SimpleDate(2082, 1, 1), 5, provider, weekend=frozenset({6, 7}))  # SimpleDate(2082, 1, 8)
```

`working_days_between` counts the half-open range `[start, end)`. `add_working_days(date, 0)`
returns the date unchanged even if it is a closure; use `next_working_day` to adjust onto a working
day. The same three helpers are also available as static methods on `NepaliDateConverter`.

**A policy** states the week an institution keeps and the events it names together, and every
helper accepts one in place of a provider:

```python
office = NepaliCalendarPolicy(provider=provider)            # closed Saturdays, Nepal's usual week
school = NepaliCalendarPolicy(frozenset({7, 1}), provider)  # closed Saturday and Sunday

school.status_of(SimpleDate(2082, 1, 1))            # NepaliDayStatus
school.status_of(SimpleDate(2082, 1, 1)).names      # ['नयाँ वर्ष']
school.month_status(2082, 1)                        # one NepaliDayStatus per day, index 0 is day 1
school.is_non_working_day(SimpleDate(2082, 1, 1))   # True
school.events_on(SimpleDate(2082, 1, 1))            # events on one day, strongest kind first
school.events_in(2082, 1)                           # every event in a month, in date order

next_working_day(SimpleDate(2082, 1, 1), school)    # the policy carries its own weekend
```

Pass a policy or a provider-and-weekend pair, never both: the helpers raise `ValueError` if you do.

`NepaliDayStatus` answers what one day is: `is_weekly_off`, `events`, `is_non_working`,
`primary_kind`, `names` and `closures`. Marking a day and refusing it stay separate decisions, so a
policy blocks nothing until you ask it to:

```python
selectable = school.as_selectable_dates()

# Or compose the wrappers yourself
selectable = excluding_closures(excluding_weekends(NepaliSelectableDates()), provider)
```

**Multi-day spans.** An event covers exactly one day, so a festival or a stretch of leave expands to
one entry per day, each carrying everything but the date unchanged:

```python
NepaliCalendarEvent(SimpleDate(2082, 6, 17), "Dashain", NepaliEventKind.RELIGIOUS,
                    id="dashain-2082").spanning_days(10)              # 10 events

NepaliCalendarEvent(SimpleDate(2082, 6, 17), "Annual leave",
                    NepaliEventKind.OBSERVANCE).spanning_through(SimpleDate(2082, 6, 26))   # 10 events
```

Give the event an `id` first when the days have to be recognized as one thing again.

## Interoperating with Kotlin, Swift and JavaScript clients

This package is a port of the `:core` module of the sibling
[Nepali-Date-Picker](https://github.com/shivathapaa/Nepali-Date-Picker) project, so a payload
written here reads on any of its platforms. The conversion tables, every conversion result, and the
wire strings below are identical across them.

The Kotlin side has an optional `kotlinx-serialization` artifact that defines these shapes. There is
no Python counterpart and none is needed: dataclasses and `json` produce the same bytes.

| Type | On the wire | Produce it here with |
| --- | --- | --- |
| `SimpleDate` | `"2082-02-14"` | `NepaliDateFormatter.format(date, DatePattern.YYYY_DASH_MM_DASH_DD)` |
| `SimpleDate` (struct form) | `{"year": 2082, "month": 2, "dayOfMonth": 14}` | `dataclasses.asdict`, renaming `day_of_month` |
| `SimpleTime` | `"09:30:00"`, `"23:59:59.123456789"` | `NepaliTimeFormatter.format(time)` |
| `CustomCalendar` | 12-field object: `year`, `month`, `dayOfMonth`, `era`, `firstDayOfMonth`, `lastDayOfMonth`, `totalDaysInMonth`, `dayOfWeekInMonth`, `dayOfWeek`, `dayOfYear`, `weekOfMonth`, `weekOfYear` | `dataclasses.asdict`, camel-casing the keys |
| `CalendarSystem` | `1` for Gregorian, `2` for Bikram Sambat | `system.era` |
| `NepaliCalendarEvent` | `{"date": "2082-01-01", "name": "...", "kind": "GovernmentPublic"}`, plus `closesOffices`, `id` and `payload` when set | see the note on `kind` below |
| `NepaliDayStatus` | `{"isWeeklyOff": false, "events": [...]}` | `is_weekly_off` plus each event written as above |

The last five `CustomCalendar` fields are optional going back into Kotlin and default to `-1`, so a
payload that omits them still decodes. When all you mean is a day, send the `SimpleDate` string
rather than a whole calendar record.

**Field names differ by convention.** This package is snake_case and the others are camelCase, so
`day_of_month` travels as `dayOfMonth`. Convert at the boundary; nothing in the values changes.

**`kind` needs translating.** Kotlin writes the enum's own name, `GovernmentPublic`, `Religious`,
`Regional`, `Observance`. This package spells the same members `GOVERNMENT_PUBLIC`, `RELIGIOUS`,
`REGIONAL`, `OBSERVANCE`, and the Swift and JavaScript APIs use `governmentPublic`. Kotlin rejects a
name it does not know rather than guessing, since the guess would decide whether a day closes an
office:

```python
_TO_WIRE = {
    NepaliEventKind.GOVERNMENT_PUBLIC: "GovernmentPublic",
    NepaliEventKind.RELIGIOUS: "Religious",
    NepaliEventKind.REGIONAL: "Regional",
    NepaliEventKind.OBSERVANCE: "Observance",
}
_FROM_WIRE = {wire: kind for kind, wire in _TO_WIRE.items()}
```

**A span is many entries.** A Kotlin event covers exactly one day, so something that runs longer
travels as one entry per day sharing an `id`. `spanning_days` and `spanning_through` already build
that shape; collapse it back with `id` on the way in.

## Migrating from 3.0.0

The holiday API became the event API in 3.1.0, because a holiday is one kind of calendar event. The
former names still resolve and still work, including providers written against
`NepaliHolidayProvider`; importing from `nepali_calendar_utils.holiday` raises a
`DeprecationWarning` naming the replacement.

| 3.0.0 | 3.1.0 |
| --- | --- |
| `HolidayEntry` | `NepaliCalendarEvent` |
| `HolidayKind` | `NepaliEventKind` |
| `NepaliHolidayProvider` | `NepaliEventProvider` |
| `NoOpHolidayProvider` | `NoOpEventProvider` |
| `provider.holidays(year)` | `provider.events(year)` |
| `provider.is_holiday(date)` | `provider.closes_on(date)` |
| `excluding_holidays(base, provider)` | `excluding_closures(base, provider)` |
| `nepali_calendar_utils.holiday` | `nepali_calendar_utils.event` |

`NepaliWeekend` moved packages without being renamed. `from nepali_calendar_utils import *` no
longer binds the former names, since `__all__` now lists the event surface; import them explicitly
if you still need them.

## Documentation

The full API reference is published at
**[shivathapaa.github.io/nepali_calendar_utils](https://shivathapaa.github.io/nepali_calendar_utils/)**,
generated from the source docstrings.

- [`NepaliDateConverter`](https://shivathapaa.github.io/nepali_calendar_utils/api/converter.html) - the main facade: conversion, formatting, comparison, digit scripts, selectable-date factories, working-day helpers.
- [Data types](https://shivathapaa.github.io/nepali_calendar_utils/api/data.html) - `CustomCalendar`, `SimpleDate`, `SimpleTime`, `NepaliMonthCalendar`, `MonthCalendar`, `CalendarSystem`, `DigitScript`, `NepaliDateFormatter`, `NepaliTimeFormatter`, locale types.
- [Events and working days](https://shivathapaa.github.io/nepali_calendar_utils/api/event.html) - `NepaliEventProvider`, `NepaliCalendarEvent`, `NepaliCalendarPolicy`, `NepaliDayStatus`, spans and working-day arithmetic.
- [Selectable dates](https://shivathapaa.github.io/nepali_calendar_utils/api/selectable_dates.html) - `NepaliSelectableDates`.

Release notes live on the [releases page](https://github.com/shivathapaa/nepali_calendar_utils/releases).

## Other platforms and a date picker UI

This package is the **Python** port of the [Nepali Date Picker](https://github.com/shivathapaa/Nepali-Date-Picker)
calendar core. The same tables are ported to Kotlin, Swift and JavaScript, so conversions match
across all four, and every other platform ships a ready-made picker UI that this package
deliberately does not:

| Platform | Guide | Packages |
| --- | --- | --- |
| **Python / backend** | This README | [PyPI](https://pypi.org/project/nepali_calendar_utils/) |
| **Kotlin / Android / KMP** | [main README](https://github.com/shivathapaa/Nepali-Date-Picker/blob/main/README.md) | `io.github.shivathapaa:nepali-date-picker-ui` (Material3 pickers) and `:nepali-date-picker-core` (engine only) on [Maven Central](https://central.sonatype.com/namespace/io.github.shivathapaa) |
| **Swift / iOS** | [README-spm.md](https://github.com/shivathapaa/Nepali-Date-Picker/blob/main/README-spm.md) | [Nepali-Date-Picker-SPM](https://github.com/shivathapaa/Nepali-Date-Picker-SPM) |
| **JavaScript / TypeScript / web** | [README-js.md](https://github.com/shivathapaa/Nepali-Date-Picker/blob/main/README-js.md) | [`@nepali-date-picker/web-component`](https://www.npmjs.com/package/@nepali-date-picker/web-component) (framework-agnostic elements) and [`@nepali-date-picker/core`](https://www.npmjs.com/package/@nepali-date-picker/core) (engine only, the JavaScript counterpart of this package) |

Live demos: the [Compose demo](https://shivathapaa.github.io/Nepali-Date-Picker/) and the
[web-component demo](https://shivathapaa.github.io/Nepali-Date-Picker/demo/).

## Support

You can contribute to this project in several ways:

- Have an idea for an improvement or a new feature? I'm open to suggestions! Feel free to suggest changes, request enhancements, or report issues [here](https://github.com/shivathapaa/nepali_calendar_utils/issues/new/choose).
- Share the project with your network to help others discover it.
- Want to contribute directly? You're welcome to open a pull request! Be sure to review the [CONTRIBUTING.md](https://github.com/shivathapaa/nepali_calendar_utils/blob/main/CONTRIBUTING.md) guide before getting started.
- Show your support by giving this repository a Star⭐. It means a lot! 😊

## License

This project is licensed under the [Mozilla Public License 2.0 (MPL 2.0)](https://github.com/shivathapaa/nepali_calendar_utils/blob/main/LICENSE),
a permissive open-source license that lets you use, modify and distribute the code, provided that
modifications to the MPL-licensed files are made available under the same license.

To keep improvements to the core library open and useful to everyone: any modification you make to
the files of this library is subject to the terms of the license, and if you modify the library you
must make the source of your modifications available to all recipients of the modified library under
those same terms.

For the full text, see the [LICENSE](https://github.com/shivathapaa/nepali_calendar_utils/blob/main/LICENSE) file.
