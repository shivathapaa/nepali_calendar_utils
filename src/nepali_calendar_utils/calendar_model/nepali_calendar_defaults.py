from nepali_calendar_utils.data.custom_calendar import CustomCalendar, SimpleDate
from nepali_calendar_utils.data.nepali_date_locale import *

_MONTHS_IN_YEAR = 12


class _NepaliCalendarDefaultsMeta(type):
    """Carries GregorianYearRange as a lazily computed attribute.

    The value needs the converter, and the converter imports this module, so it cannot be
    computed while this class body runs. Reading it the first time resolves it and caches it,
    which keeps ``NepaliCalendarDefaults.GregorianYearRange`` readable as a plain attribute.
    """

    _gregorian_year_range = None

    @property
    def GregorianYearRange(cls) -> range:
        """English years spanned by the default NepaliYearRange."""
        if cls._gregorian_year_range is None:
            cls._gregorian_year_range = cls._compute_gregorian_year_range(cls.NepaliYearRange)
        return cls._gregorian_year_range


class NepaliCalendarDefaults(metaclass=_NepaliCalendarDefaultsMeta):
    FIRST_DAY_OF_WEEK = 1

    DefaultLocale = NepaliDateLocale()

    DefaultRangePickerLocale = NepaliDateLocale(month_name=NameFormat.SHORT)

    DateFormatStyle = NepaliDateFormatStyle.SHORT_YMD

    EnglishYearRange = range(1913, 2044)
    NepaliYearRange = range(1970, 2101)

    startingNepaliCalendar = CustomCalendar(
        year=NepaliYearRange.start,
        month=1,
        day_of_month=1,
        total_days_in_month=31,
        day_of_week_in_month=1,
        day_of_week=1,
        day_of_year=1,
        week_of_month=1,
        era=2,
        week_of_year=1,
        first_day_of_month=1,  # Sunday
        last_day_of_month=3    # Tuesday
    )

    endNepaliCalendar = CustomCalendar(
        year=2100,
        month=12,
        day_of_month=31,
        era=2,
        first_day_of_month=2,
        last_day_of_month=4,
        total_days_in_month=31,
        day_of_week_in_month=5,
        day_of_week=4,
        day_of_year=366,
        week_of_month=5,
        week_of_year=53
    )

    startingEnglishCalendar = CustomCalendar(
        year=EnglishYearRange.start,
        month=4,
        day_of_month=13,
        total_days_in_month=30,
        day_of_week_in_month=2,
        day_of_week=1,
        day_of_year=103,
        week_of_month=3,
        era=1,
        week_of_year=16,
        first_day_of_month=3,  # Tuesday
        last_day_of_month=4    # Wednesday
    )

    # Earliest English date that converts, matching startingEnglishCalendar. The two calendars
    # start mid-year relative to each other, so EnglishYearRange alone is not a sufficient bound:
    # 1913-01-01 through 1913-04-12 sit inside the year range yet have no Bikram Sambat
    # equivalent. A Gregorian grid shows those days disabled rather than hiding the month.
    minConvertibleEnglishDate = SimpleDate(
        year=startingEnglishCalendar.year,
        month=startingEnglishCalendar.month,
        day_of_month=startingEnglishCalendar.day_of_month,
    )

    # Latest English date that converts: the last day of EnglishYearRange. endNepaliCalendar
    # reaches into 2044, but the converter refuses English years past EnglishYearRange, so this
    # is the real ceiling for a Gregorian-first caller.
    maxConvertibleEnglishDate = SimpleDate(
        year=EnglishYearRange[-1],
        month=12,
        day_of_month=31,
    )

    @classmethod
    def gregorian_year_range_for(cls, nepali_year_range: range) -> range:
        """The English years covering a given Bikram Sambat ``nepali_year_range``, so both
        calendars page over the same span of real days.

        The result is clamped into EnglishYearRange: the tail of NepaliYearRange reaches into an
        English year the converter rejects. Returns an empty range for an empty input.
        """
        if nepali_year_range == cls.NepaliYearRange:
            return cls.GregorianYearRange
        return cls._compute_gregorian_year_range(nepali_year_range)

    @classmethod
    def _compute_gregorian_year_range(cls, nepali_year_range: range) -> range:
        if len(nepali_year_range) == 0:
            return range(0, 0)

        # Imported here because the converter reads this module while it is being defined.
        from nepali_calendar_utils.calendar_model.date_converters import DateConverters

        supported = cls.NepaliYearRange
        first_nepali_year = min(max(nepali_year_range[0], supported[0]), supported[-1])
        last_nepali_year = min(max(nepali_year_range[-1], supported[0]), supported[-1])
        last_month_length = DateConverters.get_total_days_in_nepali_month(
            last_nepali_year, _MONTHS_IN_YEAR
        )

        first_english_year = DateConverters.convert_to_english_calendar(first_nepali_year, 1, 1).year
        last_english_year = DateConverters.convert_to_english_calendar(
            last_nepali_year, _MONTHS_IN_YEAR, last_month_length
        ).year

        return range(
            max(first_english_year, cls.EnglishYearRange[0]),
            min(last_english_year, cls.EnglishYearRange[-1]) + 1,
        )
