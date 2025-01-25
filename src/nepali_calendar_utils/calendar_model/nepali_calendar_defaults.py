from nepali_calendar_utils.data.custom_calendar import CustomCalendar
from nepali_calendar_utils.data.nepali_date_locale import *

class NepaliCalendarDefaults:
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
