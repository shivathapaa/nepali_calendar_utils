# nepali_calendar_utils

Utilities for working with Nepali (Bikram Sambat) dates: BS to AD conversion, month
details, locale-aware formatting, date arithmetic, digit-script localization, a
text-field date formatter, and a holiday provider SPI with working-day helpers.

This is the pure-Python port of the `:core` module of the sibling Kotlin Multiplatform
project, [Nepali-Date-Picker](https://github.com/shivathapaa/Nepali-Date-Picker). The
conversion tables and utility semantics are kept in sync across both libraries.

## Install

```bash
pip install nepali_calendar_utils
```

## Quick start

```python
from nepali_calendar_utils import NepaliDateConverter

converter = NepaliDateConverter()
nepali = converter.convert_english_to_nepali(2024, 6, 21)
print(nepali.year, nepali.month, nepali.day_of_month)
```

## Conventions

- **1-based indexing**: month / weekday 1 = Baisakh / Sunday, 12 = Chaitra, 7 = Saturday.
- `era`: 1 = AD, 2 = BS.
- Weekend is Saturday-only by default.
- Supported range: BS 1970..2100, AD 1913..2043.

```{toctree}
:maxdepth: 2
:caption: Contents

api/index
```
