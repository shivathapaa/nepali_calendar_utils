from datetime import datetime
from zoneinfo import ZoneInfo
from nepali_calendar_utils.data.custom_calendar import *
from nepali_calendar_utils.data.nepali_date_locale import *
from nepali_calendar_utils.calendar_model.date_converters import DateConverters

class NepaliCalendarModel:
    def __init__(self, locale: NepaliDateLocale = NepaliDateLocale()):
        self.locale = locale
        self.time_zone = ZoneInfo("Asia/Kathmandu")
        self.local_english_date_time = datetime.now(self.time_zone)
        
    @property
    def today_nepali_calendar(self) -> CustomCalendar:
        return self.get_nepali_date_instance()
    
    @property
    def today_english_calendar(self) -> CustomCalendar:
        today_nepali_calendar = NepaliCalendarModel().today_nepali_calendar
        return DateConverters.convert_to_english_date(nepali_yyyy=today_nepali_calendar.year, nepali_mm=today_nepali_calendar.month, nepali_dd=today_nepali_calendar.day_of_month)

    @property
    def today_english_simple_date(self) -> SimpleDate:
        return SimpleDate(
            year=self.local_english_date_time.year,
            month=self.local_english_date_time.month,
            day_of_month=self.local_english_date_time.day,
        )
    
    @property
    def current_time(self) -> SimpleTime:
        now_time = datetime.now(self.time_zone)
        return SimpleTime(
            hour=now_time.hour,
            minute=now_time.minute,
            second=now_time.second,
            nanosecond=now_time.microsecond * 1000,  # Convert microseconds to nanoseconds
        )

    def get_nepali_date_instance(self) -> CustomCalendar:
        return DateConverters.convert_to_nepali_calendar(
            englishYYYY=self.local_english_date_time.year,
            englishMM=self.local_english_date_time.month,
            englishDD=self.local_english_date_time.day,
        )
        
    @staticmethod
    def convert_to_nepali_calendar(english_year, english_month, english_day) -> CustomCalendar:
        return DateConverters.convert_to_nepali_calendar(english_year, english_month, english_day)


    @staticmethod
    def convert_to_english_date(nepali_year, nepali_month, nepali_day) -> CustomCalendar:
        return DateConverters.convert_to_english_date(nepali_year, nepali_month, nepali_day)

    @staticmethod
    def get_total_days_in_nepali_month(year, month):
        return DateConverters.get_total_days_in_nepali_month(year, month)

    @staticmethod
    def get_total_days_in_english_month(year, month):
        return DateConverters.get_total_days_in_english_month(year, month)

    @staticmethod
    def get_nepali_month(nepali_year, nepali_month):
        return DateConverters.calculate_nepali_month_details(nepali_year, nepali_month)

    @staticmethod
    def get_nepali_calendar(simple_nepali_date):
        return DateConverters.get_nepali_calendar(simple_nepali_date)

    @staticmethod
    def parse(date_string):
        if len(date_string) != 8:
            return None

        try:
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:8])

            if month < 1 or month > 12 or day < 1 or day > 32:
                return None  # Invalid month or day

            return DateConverters.get_nepali_calendar({"year": year, "month": month, "day": day})
        except ValueError:
            return None  # Invalid numeric values
        except Exception as e:
            return {"year": year, "month": month, "day": day, "status": -1}  # Error

    @staticmethod
    def remove_slash_delimiter(date_with_delimiter):
        return date_with_delimiter.replace("/", "")

    @staticmethod
    def add_or_subtract_days_to_simple_date(year, month, day_of_month, days_to_adjust):
        return DateConverters.adjust_nepali_date_for_day_adjustments(year, month, day_of_month, days_to_adjust)

    @staticmethod
    def plus_nepali_months(from_nepali_calendar, added_months_count) -> NepaliMonthCalendar:
        return DateConverters.get_nepali_month(
            from_nepali_calendar.year, from_nepali_calendar.month, added_months_count
        )

    @staticmethod
    def minus_nepali_months(from_nepali_calendar, subtracted_months_count) -> NepaliMonthCalendar:
        return DateConverters.get_nepali_month(
            from_nepali_calendar.year, from_nepali_calendar.month, -subtracted_months_count
        )
        
    @staticmethod
    def nepali_days_in_between(start_date, end_date) -> int:
        return DateConverters.nepali_days_in_between(start_date, end_date)
        
    @staticmethod
    def format_nepali_date(year, month, day_of_month, day_of_week, locale: NepaliDateLocale) -> str:
        show_month_name = locale.date_format in [
            NepaliDateFormatStyle.FULL,
            NepaliDateFormatStyle.LONG,
            NepaliDateFormatStyle.MEDIUM
        ]

        weekday = locale.language.weekdays[day_of_week - 1]
        localized_month = locale.language.months[month - 1]

        weekday_name = {
            NameFormat.FULL: weekday.full,
            NameFormat.MEDIUM: weekday.medium,
            NameFormat.SHORT: weekday.short,
        }[locale.week_day_name]

        month_name = {
            NameFormat.SHORT: localized_month.short,
        }.get(locale.month_name, localized_month.full)

        day = NepaliCalendarModel.localize_number(
            str(day_of_month) if show_month_name else str(day_of_month).zfill(2),
            locale.language
        )

        month_num = NepaliCalendarModel.localize_number(str(month).zfill(2), locale.language)
        localized_year = NepaliCalendarModel.localize_number(str(year), locale.language)
        short_year = localized_year[-2:]

        return {
            NepaliDateFormatStyle.FULL: f"{weekday_name}, {month_name} {day}, {localized_year}",
            NepaliDateFormatStyle.LONG: f"{month_name} {day}, {localized_year}",
            NepaliDateFormatStyle.MEDIUM: f"{localized_year} {month_name} {day}",
            NepaliDateFormatStyle.SHORT_MDY: f"{month_num}/{day}/{localized_year}",
            NepaliDateFormatStyle.SHORT_YMD: f"{localized_year}/{month_num}/{day}",
            NepaliDateFormatStyle.COMPACT_MDY: f"{month_num}/{day}/{short_year}",
            NepaliDateFormatStyle.COMPACT_YMD: f"{short_year}/{month_num}/{day}",
        }[locale.date_format]

    @staticmethod
    def format_nepali_date_from_calendar(custom_calendar: CustomCalendar, locale: NepaliDateLocale):
        NepaliCalendarModel.validate_nepali_date(custom_calendar.year, custom_calendar.month, custom_calendar.day_of_month)

        return NepaliCalendarModel.format_nepali_date(
            year=custom_calendar.year,
            month=custom_calendar.month,
            day_of_month=custom_calendar.day_of_month,
            day_of_week=custom_calendar.day_of_week,
            locale=locale
        )

    @staticmethod
    def format_english_date(year, month, day_of_month, day_of_week, locale: NepaliDateLocale) -> str:
        language = locale.language
        show_month_name = locale.date_format in [
            NepaliDateFormatStyle.FULL,
            NepaliDateFormatStyle.LONG,
            NepaliDateFormatStyle.MEDIUM
        ]

        weekday = language.weekdays[day_of_week - 1]
        localized_month = language.english_months[month - 1]

        weekday_name = {
            NameFormat.FULL: weekday.full,
            NameFormat.MEDIUM: weekday.medium,
            NameFormat.SHORT: weekday.short,
        }[locale.week_day_name]

        month_name = {
            NameFormat.SHORT: localized_month.short,
        }.get(locale.month_name, localized_month.full)

        day = NepaliCalendarModel.localize_number(
            str(day_of_month) if show_month_name else str(day_of_month).zfill(2),
            language
        )

        month_num = NepaliCalendarModel.localize_number(str(month).zfill(2), language)
        full_year = NepaliCalendarModel.localize_number(str(year), language)
        short_year = full_year[-2:]

        return {
            NepaliDateFormatStyle.FULL: f"{weekday_name}, {month_name} {day}, {full_year}",
            NepaliDateFormatStyle.LONG: f"{month_name} {day}, {full_year}",
            NepaliDateFormatStyle.MEDIUM: f"{full_year} {month_name} {day}",
            NepaliDateFormatStyle.SHORT_MDY: f"{month_num}/{day}/{full_year}",
            NepaliDateFormatStyle.SHORT_YMD: f"{full_year}/{month_num}/{day}",
            NepaliDateFormatStyle.COMPACT_MDY: f"{month_num}/{day}/{short_year}",
            NepaliDateFormatStyle.COMPACT_YMD: f"{short_year}/{month_num}/{day}",
        }[locale.date_format]

    @staticmethod
    def format_english_date_nepali_time_to_iso_format(english_date: SimpleDate, time: SimpleTime) -> str:
        kathmandu_tz = ZoneInfo("Asia/Kathmandu")
        local_datetime = datetime(
            english_date.year,
            english_date.month,
            english_date.day_of_month,
            time.hour,
            time.minute,
            time.second,
            time.nanosecond // 1000,
            tzinfo=kathmandu_tz
        )    
        utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))
        return utc_datetime.isoformat().replace("+00:00", "Z")
    
    @staticmethod
    def format_nepali_date_time_to_iso_format(nepali_date: SimpleDate, time: SimpleTime) -> str:
        kathmandu_tz = ZoneInfo("Asia/Kathmandu")
        converted_english_date = NepaliCalendarModel.convert_to_english_date(
            nepali_date.year, nepali_date.month, nepali_date.day_of_month
        )
        local_datetime = datetime(
            converted_english_date.year,
            converted_english_date.month,
            converted_english_date.day_of_month,
            time.hour,
            time.minute,
            time.second,
            time.nanosecond // 1000,
            tzinfo=kathmandu_tz
        )
        utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))
        return utc_datetime.isoformat().replace("+00:00", "Z")

    @staticmethod
    def compare_dates_custom(calendar: CustomCalendar, year, month, day_of_month):
        if calendar.year != year:
            return calendar.year - year
        elif calendar.month != month:
            return calendar.month - month
        else:
            return calendar.day_of_month - day_of_month

    @staticmethod
    def compare_dates_simple(simple_date: SimpleDate, year, month, day_of_month):
        if simple_date.year != year:
            return simple_date.year - year
        elif simple_date.month != month:
            return simple_date.month - month
        else:
            return simple_date.day_of_month - day_of_month

    @staticmethod
    def validate_nepali_date(year, month, day):
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month value: {month}. Must be between 1 and 12.")

        max_days_in_month = NepaliCalendarModel.get_total_days_in_nepali_month(year, month)
        if day < 1 or day > max_days_in_month:
            raise ValueError(f"Invalid day value: {day}. Must be between 1 and {max_days_in_month} for month {month}.")

    @staticmethod
    def get_nepali_month_name(month_of_year, format: NameFormat, language: NepaliCalendarUtilsLang):
        if month_of_year < 1 or month_of_year > 12:
            raise ValueError(f"Invalid monthOfYear value: {month_of_year}. Must be between 1 and 12.")
        month = language.months[month_of_year - 1]
        return month.short if format == NameFormat.SHORT else month.full

    @staticmethod
    def get_english_month_name(month, language: NepaliCalendarUtilsLang, format: NameFormat):
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month value: {month}. Must be between 1 and 12.")
        month_index = language.english_months[month - 1]
        return month_index.short if format == NameFormat.SHORT else month_index.full

    @staticmethod
    def date_pattern_as_input_format(locale_format):
        pattern_with_delimiters = (
            locale_format
            .replace(r"[^dMy/]", "")
            .replace(r"d{1,2}", "dd")
            .replace(r"M{1,2}", "MM")
            .replace(r"y{1,4}", "yyyy")
            .replace("My", "M/y")
            .replace(r"[.-]", "/")  # Replace other delimiters with /
        )
        return pattern_with_delimiters

    @staticmethod
    def localize_number(string_to_localize: str, lang: NepaliCalendarUtilsLang):
        return string_to_localize if lang == NepaliCalendarUtilsLang.ENGLISH else NepaliCalendarModel.convert_to_nepali_number(string_to_localize)

    @staticmethod
    def localize_numbers_to_nepali(english_string: str):
        return NepaliCalendarModel.convert_to_nepali_number(english_string)

    @staticmethod
    def localize_number_to_english(nepali_string: str):
        return NepaliCalendarModel.convert_to_english_number(nepali_string)


    NEPALI_DIGITS = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']
    NEPALI_TO_ENGLISH_DIGITS = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }

    @staticmethod
    def convert_to_nepali_number(string: str):
        return ''.join(
            NepaliCalendarModel.NEPALI_DIGITS[int(char)] if '0' <= char <= '9' else char
            for char in string
        )

    @staticmethod
    def convert_to_english_number(string: str):
        return ''.join(
            NepaliCalendarModel.NEPALI_TO_ENGLISH_DIGITS.get(char, char) for char in string
        )
