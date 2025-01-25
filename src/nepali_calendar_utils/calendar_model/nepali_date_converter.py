from nepali_calendar_utils.data.custom_calendar import *
from nepali_calendar_utils.calendar_model.nepali_calendar_model import NepaliCalendarModel
from datetime import date
from nepali_calendar_utils.data.nepali_date_locale import NameFormat, NepaliDateLocale, NepaliCalendarUtilsLang

class NepaliDateConverter:
    """A utility class for handling Nepali date conversions, formatting, and related operations."""

    def __init__(self):
        self.calendar_model = NepaliCalendarModel()

    @property
    def today_nepali_calendar(self) -> CustomCalendar:
        """Returns today's date in the Nepali calendar as a CustomCalendar."""
        return self.calendar_model.today_nepali_calendar

    @property
    def today_english_calendar(self) -> CustomCalendar:
        """Returns today's date in the English calendar as a CustomCalendar."""
        return self.calendar_model.today_english_calendar

    @property
    def today_nepali_simple_date(self) -> SimpleDate:
        """Returns today's date in the Nepali calendar as a SimpleDate."""
        return self.calendar_model.today_nepali_calendar.to_simple_date()
    
    @property
    def today_english_simple_date(self) -> SimpleDate:
        """Returns today's date in the English calendar as a SimpleDate."""
        return self.calendar_model.today_english_simple_date

    @property
    def current_time(self) -> SimpleTime:
        """Returns the current time in Asia/Kathmandu timezone as a SimpleTime object."""
        return self.calendar_model.current_time

    @staticmethod
    def convert_english_to_nepali(english_yyyy: int, english_mm: int, english_dd: int) -> CustomCalendar:
        """
        Converts an English date to a Nepali date.

        Args:
            english_yyyy (int): Year in English calendar.
            english_mm (int): Month in English calendar (1-12).
            english_dd (int): Day in English calendar (1-31).

        Returns:
            CustomCalendar: Corresponding Nepali date.
        """
        calendar_model = NepaliCalendarModel()
        return calendar_model.convert_to_nepali_calendar(english_yyyy, english_mm, english_dd)

    @staticmethod
    def convert_nepali_to_english(nepali_yyyy: int, nepali_mm: int, nepali_dd: int) -> CustomCalendar:
        """
        Converts a Nepali date to an English date.

        Args:
            nepali_yyyy (int): Year in Nepali calendar.
            nepali_mm (int): Month in Nepali calendar (1-12).
            nepali_dd (int): Day in Nepali calendar (1-32).

        Returns:
            CustomCalendar: Corresponding English date.
        """
        calendar_model = NepaliCalendarModel()
        return calendar_model.convert_to_english_date(nepali_yyyy, nepali_mm, nepali_dd)

    @staticmethod
    def get_nepali_calendar(nepali_yyyy: int, nepali_mm: int, nepali_dd: int) -> CustomCalendar:
        """
        Gets the Nepali calendar representation for a specific Nepali date.

        Args:
            nepali_yyyy (int): Year in Nepali calendar.
            nepali_mm (int): Month in Nepali calendar (1-based index).
            nepali_dd (int): Day of the month (1-based index).

        Returns:
            CustomCalendar: Detailed Nepali calendar information.
        """
        return NepaliCalendarModel.get_nepali_calendar(SimpleDate(nepali_yyyy, nepali_mm, nepali_dd))

    @staticmethod
    def get_nepali_calendar_after_addition_or_subtraction(year: int, month: int, day_of_month: int, days_to_adjust: int) -> CustomCalendar:
        """
        Adjusts a given Nepali date by adding or subtracting days.

        Args:
            year (int): Nepali year.
            month (int): Nepali month (1-12).
            day_of_month (int): Nepali day of the month (1-32).
            days_to_adjust (int): Number of days to adjust (positive or negative).

        Returns:
            CustomCalendar: Adjusted Nepali date.
        """
        return NepaliCalendarModel.add_or_subtract_days_to_simple_date(year, month, day_of_month, days_to_adjust)

    @staticmethod
    def get_nepali_month_calendar(nepali_year: int, nepali_month: int) -> NepaliMonthCalendar:
        """
        Gets the details of a Nepali month.

        Args:
            nepali_year (int): Nepali year.
            nepali_month (int): Nepali month (1-12).

        Returns:
            NepaliMonthCalendar: Details of the specified Nepali month.
        """
        return NepaliCalendarModel.get_nepali_month(nepali_year, nepali_month)

    @staticmethod
    def get_total_days_in_nepali_month(year: int, month: int) -> int:
        """
        Gets the total days in a Nepali month.

        Args:
            year (int): Nepali year.
            month (int): Nepali month (1-12).

        Returns:
            int: Total days in the month.
        """
        return NepaliCalendarModel.get_total_days_in_nepali_month(year, month)

    @staticmethod
    def get_total_days_in_english_month(year: int, month: int) -> int:
        """
        Gets the total days in an English month.

        Args:
            year (int): English year.
            month (int): English month (1-12).

        Returns:
            int: Total days in the month.
        """
        return NepaliCalendarModel.get_total_days_in_english_month(year, month)
    
    @staticmethod
    def get_nepali_days_in_between(start_date: SimpleDate, end_date: SimpleDate) -> int:
        """
        Calculates the total number of days between two SimpleDate objects in the Nepali calendar.

        The end date is not included in the count. Add 1 to the returned value to include the end date.

        Args:
            start_date (SimpleDate): The starting date in the Nepali calendar.
            end_date (SimpleDate): The ending date in the Nepali calendar.

        Returns:
            int: The number of days between the two dates.
                - Throws an exception if the year is not in the range defined by NepaliDatePickerDefaults.NepaliYearRange.
                - Returns -1 if either date is invalid.

        Raises:
            ValueError: If the year of either date is out of the allowed Nepali year range.
        """
        return NepaliCalendarModel.nepali_days_in_between(start_date, end_date)
    
    from datetime import date

    @staticmethod
    def get_english_days_in_between(start_date: int, end_date: int) -> int:
        """
        Calculates the total number of days between two SimpleDate objects in the English calendar.

        The end date is not included in the count. Add 1 to the returned value to include the end date.

        Args:
            start_date (SimpleDate): The starting date.
            end_date (SimpleDate): The ending date.

        Returns:
            int: The number of days between the two dates.
        """
        start_local_date = date(start_date.year, start_date.month, start_date.day_of_month)
        end_local_date = date(end_date.year, end_date.month, end_date.day_of_month)

        return (end_local_date - start_local_date).days

    @staticmethod
    def format_nepali_date(year: int, month: int, day_of_month: int, day_of_week: int, locale: NepaliDateLocale) -> str:
        """
        Formats a Nepali date based on user preferences.(Without date validation)

        Args:
            year (int): Year of the date.
            month (int): Month of the date.
            day_of_month (int): Day of the month.
            day_of_week (int): Day of the week.
            locale (NepaliDateLocale): User preferences for formatting.

        Returns:
            str: Formatted date string.
        """
        return NepaliCalendarModel.format_nepali_date(year, month, day_of_month, day_of_week, locale)

    @staticmethod
    def format_nepali_date_from_calendar(custom_calendar: CustomCalendar, locale: NepaliDateLocale) -> str:
        """
        Overload to format a Nepali date from a CustomCalendar object.

        Formats a Nepali date based on user preferences. (With date validation)
        
        Args:
            custom_calendar (CustomCalendar): Calendar object containing date details.
            locale (NepaliDateLocale): User preferences for formatting.

        Returns:
            str: Formatted date string.
        """
        return NepaliCalendarModel.format_nepali_date_from_calendar(custom_calendar=custom_calendar, locale=locale)
        
    @staticmethod
    def format_english_date(year: int, month: int, day_of_month: int, day_of_week: int, locale: NepaliDateLocale) -> str:
        """
        Formats an English date based on the specified user preferences.

        Args:
            year (int): Year of the date.
            month (int): Month of the date.
            day_of_month (int): Day of the month.
            day_of_week (int): Day of the week.
            locale (NepaliDateLocale): Locale specifying language, format preferences.

        Returns:
            str: Formatted date string.
        """
        return NepaliCalendarModel.format_english_date(
            year=year,
            month=month,
            day_of_month=day_of_month,
            day_of_week=day_of_week,
            locale=locale,
        )

    @staticmethod
    def format_english_date_from_calendar(custom_calendar: CustomCalendar, locale: NepaliDateLocale) -> str:
        """
        Formats an English date based on user preferences using a CustomCalendar object.

        Args:
            custom_calendar (CustomCalendar): Calendar object with date details.
            locale (NepaliDateLocale): Locale specifying language, format preferences.

        Returns:
            str: Formatted date string.
        """
        return NepaliCalendarModel.format_english_date(
            year=custom_calendar.year,
            month=custom_calendar.month,
            day_of_month=custom_calendar.day_of_month,
            day_of_week=custom_calendar.day_of_week,
            locale=locale,
        )

    @staticmethod
    def get_weekday_name(day_of_week: int, format=NameFormat.FULL, language: NepaliCalendarUtilsLang=NepaliCalendarUtilsLang.ENGLISH):
        """
        Retrieves the name of a weekday in the specified format and language.

        Args:
            day_of_week (int): Day of the week (1-7).
            format (str): Format of the name (SHORT, MEDIUM, FULL).
            language (NepaliDatePickerLang): Language for the weekday name.

        Returns:
            str: Weekday name.

        Raises:
            ValueError: If day_of_week is not between 1 and 7.
        """
        if day_of_week < 1 or day_of_week > 7:
            raise ValueError(f"Invalid day_of_week value: {day_of_week}. Must be between 1 and 7.")

        weekdays = language.weekdays[day_of_week - 1]
        return {
            NameFormat.SHORT: weekdays.short,
            NameFormat.MEDIUM: weekdays.medium,
            NameFormat.FULL: weekdays.full,
        }.get(format, weekdays.full)

    @staticmethod
    def get_month_name(month: int, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.ENGLISH) -> str:
        """
        Retrieves the name of a Nepali month in the specified format and language.

        Args:
            month (int): Month of the year (1-12).
            format (str): Format of the name (SHORT, FULL).
            language (NepaliDatePickerLang): Language for the month name.

        Returns:
            str: Month name.

        Raises:
            ValueError: If month is not between 1 and 12.
        """
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month value: {month}. Must be between 1 and 12.")

        return NepaliCalendarModel.get_nepali_month_name(month, format, language)

    @staticmethod
    def get_english_month_name(month: int, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.ENGLISH) -> str:
        """
        Retrieves the name of an English month in the specified format.

        Args:
            month (int): Month of the year (1-12).
            format (str): Format of the name (SHORT, FULL).
            language (NepaliDatePickerLang): Language for the month name.

        Returns:
            str: Month name.

        Raises:
            ValueError: If month is not between 1 and 12.
        """
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month value: {month}. Must be between 1 and 12.")

        return NepaliCalendarModel.get_english_month_name(month, language, format)

    @staticmethod
    def get_formatted_time_in_english(simple_time: SimpleTime, use_12_hour_format=True) -> str:
        """
        Formats a SimpleTime object into a time string in English.

        Args:
            simple_time (SimpleTime): The time object to format.
            use_12_hour_format (bool): Use 12-hour format if True, 24-hour otherwise.

        Returns:
            str: Formatted time string.
        """
        if use_12_hour_format:
            am_pm = "AM" if simple_time.hour < 12 else "PM"
            standard_hour = (
                12 if simple_time.hour == 0 else
                simple_time.hour - 12 if simple_time.hour > 12 else
                simple_time.hour
            )
            return f"{standard_hour}:{str(simple_time.minute).zfill(2)} {am_pm}"
        else:
            return f"{simple_time.hour}:{str(simple_time.minute).zfill(2)}"

    @staticmethod
    def get_formatted_time_in_nepali(simple_time: SimpleTime, use_12_hour_format=True) -> str:
        """
        Formats a SimpleTime object into a Nepali time string.

        Args:
            simple_time (SimpleTime): The time object to format.
            use_12_hour_format (bool): Use 12-hour format if True, 24-hour otherwise.

        Returns:
            str: Formatted time string in Nepali.
        """
        period = (
            "बिहान" if 3 <= simple_time.hour <= 11 else
            "दिउँसो" if 12 <= simple_time.hour <= 16 else
            "साँझ" if 17 <= simple_time.hour <= 19 else
            "राति"
        )
        hour = (
            12 if use_12_hour_format and simple_time.hour == 0 else
            simple_time.hour - 12 if use_12_hour_format and simple_time.hour > 12 else
            simple_time.hour
        )
        formatted_hour = NepaliDateConverter.convert_to_nepali_number(f"{hour}")
        formatted_minute = NepaliDateConverter.convert_to_nepali_number(f"{str(simple_time.minute).zfill(2)}")

        return f"{period} {formatted_hour} : {formatted_minute}" if use_12_hour_format else f"{formatted_hour} : {formatted_minute}"

    @staticmethod
    def format_nepali_datetime_to_iso(nepali_date: SimpleDate, simple_time: SimpleTime = None) -> str:
        """
        Converts a Nepali (Bikram Sambat) date and time to ISO 8601 UTC format.

        The Nepali date (Bikram Sambat) is first converted to the equivalent Gregorian (English) date,
        and then the time is appended to produce a complete timestamp in UTC.

        Parameters:
            nepali_date (SimpleDate): The date in the Nepali Bikram Sambat calendar.
            simple_time (SimpleTime, optional): The time of day. Defaults to the current time.

        Returns:
            str: A string in ISO 8601 format representing the UTC date and time.
                The result is in the format `YYYY-MM-DDTHH:mm:ssZ` (Zulu time).

        Example:
            nepali_date = SimpleDate(2081, 5, 24)  # Bikram Sambat date
            time = SimpleTime(14, 30, 15, 0)
            iso_format = NepaliDateConverter.format_nepali_date_time_to_iso_format(nepali_date, time)
            print(iso_format)  # Outputs: "2024-09-09T09:00:15Z"
        """
        if simple_time is None:
            simple_time = NepaliDateConverter().current_time

        return NepaliCalendarModel.format_nepali_date_time_to_iso_format(nepali_date, simple_time)
    
    @staticmethod
    def format_english_date_nepali_time_to_iso(english_date: SimpleDate, simple_time: SimpleTime = None) -> str:
        """
        Converts an English (Gregorian) date and time to ISO 8601 UTC format.

        Parameters:
            english_date (SimpleDate): The date in the Gregorian calendar (English date).
            simple_time (SimpleTime, optional): The time of day. Defaults to the current time.

        Returns:
            str: A string in ISO 8601 format representing the UTC date and time.
                The result is in the format `YYYY-MM-DDTHH:mm:ssZ` (Zulu time).

        Example:
            english_date = SimpleDate(2024, 9, 9)
            time = SimpleTime(14, 30, 15, 0)
            iso_format = NepaliDateConverter.format_english_date_nepali_time_to_iso_format(english_date, time)
            print(iso_format)  # Outputs: "2024-09-09T09:00:15Z"
        """
        if simple_time is None:
            simple_time = NepaliDateConverter().current_time
            
        return NepaliCalendarModel.format_english_date_nepali_time_to_iso_format(english_date, simple_time)


    @staticmethod
    def compare_calendar_dates(date_to_compare_from: CustomCalendar, date_to_compare_to: CustomCalendar) -> int:
        """
        Compares two CustomCalendar instances to determine their chronological order.

        Returns:
            - A negative integer if `date_to_compare_from` is before `date_to_compare_to`.
            - Zero if they are equal.
            - A positive integer if `date_to_compare_from` is after `date_to_compare_to`.

        Parameters:
            date_to_compare_from (CustomCalendar): The first date in the comparison.
            date_to_compare_to (CustomCalendar): The second date, which `date_to_compare_from` is compared to.

        Returns:
            int: A negative integer, zero, or a positive integer as described above.
        """
        return NepaliCalendarModel.compare_dates_custom(
            date_to_compare_from, date_to_compare_to.year, date_to_compare_to.month, date_to_compare_to.day_of_month
        )
        
    @staticmethod
    def compare_simple_dates(simple_date: SimpleDate, year: int, month: int, day_of_month: int) -> int:
        """
        Compares a SimpleDate instance with a date represented by the given year, month, and day_of_month.

        Returns:
            - A negative integer if the `simple_date` is before the given date.
            - Zero if they are equal.
            - A positive integer if the `simple_date` is after the given date.

        Parameters:
            simple_date (SimpleDate): The SimpleDate instance to compare.
            year (int): The year of the date to compare with.
            month (int): The month of the date to compare with.
            day_of_month (int): The day of the month of the date to compare with.

        Returns:
            int: A negative integer, zero, or a positive integer as described above.
        """
        return NepaliCalendarModel.compare_dates_simple(
            simple_date, year, month, day_of_month
        )

    @staticmethod
    def replace_delimiter(text: str, new_delimiter: str, old_delimiter=None) -> str:
        """
        Replaces delimiters in a string with a new delimiter.

        Parameters:
            text: The input string with delimiters to replace.
            new_delimiter: The new delimiter to use in the string.
            old_delimiter: The old delimiter to replace. If None, replace all non-alphanumeric delimiters.

        Returns:
            The string with replaced delimiters.
        """
        if old_delimiter:
            return text.replace(old_delimiter, new_delimiter)
        
        return ''.join(new_delimiter if not char.isalnum() else char for char in text)

    @staticmethod
    def localize_number(number: str, lang: NepaliCalendarUtilsLang) -> str:
        """
        Localizes a number string based on the provided locale.

        Args:
            number (str): The number to localize.
            locale (NepaliDatePickerLang): The target locale.

        Returns:
            str: Localized number.
        """
        return NepaliCalendarModel.localize_number(number, lang)

    @staticmethod
    def convert_to_nepali_number(english_string: str) -> str:
        """
        Converts an English number string to Nepali digits.

        Args:
            english_string (str): English number string.

        Returns:
            str: Nepali number string.
        """
        return NepaliCalendarModel.convert_to_nepali_number(english_string)

    @staticmethod
    def convert_to_english_number(nepali_string: str) -> str:
        """
        Converts a Nepali number string to English digits.

        Args:
            nepali_string (str): Nepali number string.

        Returns:
            str: English number string.
        """
        return NepaliCalendarModel.convert_to_english_number(nepali_string)