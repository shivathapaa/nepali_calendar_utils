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
        return calendar_model.convert_to_english_calendar(nepali_yyyy, nepali_mm, nepali_dd)

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
    def get_nepali_date_time_from_iso_format(iso_date_time: str) -> CustomDateTime:
        """
        Converts ISO UTC format to CustomDateTime which represents the Nepali CustomCalendar and Nepali SimpleTime.

        :param iso_date_time: The ISO format string.
            Examples:
                - "2020-08-30T18:43:00Z"
                - "2020-08-30T18:43:00.503Z"
                - "2020-08-30T18:43:00.123456Z"
                - "2020-08-30T18:40:00+03:00"
                - "2020-08-30T18:40:00+03:30:20"
                - "2011-11-04"
                - "2011-11-04 00:05:23.283"
                - "2011-11-04 00:05:23.283+00:00"
                - "2011-11-04T00:05:23+04:00"
                
        :return: CustomDateTime representing the Nepali calendar and time.

        :raises ValueError: If the input string cannot be parsed or date boundaries are exceeded.

        Example:
            custom_nepali_dt = get_nepali_date_time_from_iso_format("2024-09-09T09:00:15Z")
            print(custom_nepali_dt)
        """
        return NepaliCalendarModel.get_nepali_date_time_from_iso_format(iso_date_time)

    @staticmethod
    def get_english_date_nepali_time_from_iso_format(iso_date_time: str) -> CustomDateTime:
        """
        Converts ISO UTC format to CustomDateTime which represents the English CustomCalendar and Nepali SimpleTime.

        :param iso_date_time: The ISO format string.
            Examples:
                - "2020-08-30T18:43:00Z"
                - "2020-08-30T18:43:00.503Z"
                - "2020-08-30T18:43:00.123456Z"
                - "2020-08-30T18:40:00+03:00"
                - "2020-08-30T18:40:00+03:30:20"
                - "2011-11-04"
                - "2011-11-04 00:05:23.283"
                - "2011-11-04 00:05:23.283+00:00"
                - "2011-11-04T00:05:23+04:00"

        :return: CustomDateTime representing the English calendar and Nepali time.

        :raises ValueError: If the input string cannot be parsed or date boundaries are exceeded.

        Example:
            custom_english_dt = get_english_date_nepali_time_from_iso_format("2024-09-09T09:00:15Z")
            print(custom_english_dt)
        """
        return NepaliCalendarModel.get_english_date_nepali_time_from_iso_format(iso_date_time)
        
    @staticmethod
    def format_time_by_unicode_pattern(
        unicode_pattern: str,
        time: SimpleTime,
        language: NepaliCalendarUtilsLang = NepaliCalendarUtilsLang.ENGLISH
    ) -> str:
        """
        Formats a time based on the specified Unicode pattern and language preferences.

        Args:
            time (SimpleTime): An object that holds the time details 
                (hour, minute, second, nanosecond).
            unicode_pattern (str): A string specifying the pattern to use for formatting 
                the date and time. The pattern supports various placeholders like "HH", "hh", 
                "mm", "ss", "SSS", "a", etc.
            language (NepaliDatePickerLang): Specifies the language for formatting the 
                date and time, including number localization and period labels (AM/PM).

        Returns:
            str: A string representing the formatted time according to the provided Unicode 
            pattern and language preferences.

        Supported Unicode pattern placeholders:
            - `HH`: Hour in 24-hour format (00–23), zero-padded (e.g., "08" or "०८")
            - `H`: Hour in 24-hour format, no padding (e.g., "8" or "८")
            - `hh`: Hour in 12-hour format (01–12), zero-padded (e.g., "01" or "०१")
            - `h`: Hour in 12-hour format, no padding (e.g., "1" or "१")
            - `mm`: Minutes, two-digit (e.g., "05" or "०५")
            - `m`: Minutes, no padding (e.g., "5" or "५")
            - `ss`: Seconds, two-digit (e.g., "09" or "०९")
            - `s`: Seconds, no padding (e.g., "9" or "९")
            - `SSSS`: Four-digit nanosecond precision (e.g., "1234" or "१२३४")
            - `SSS`: Millisecond precision (e.g., "123" or "१२३")
            - `SS`: Two-digit fractional seconds (e.g., "12" or "१२")
            - `S`: One-digit fractional second (e.g., "1" or "१")
            - `a`: Lowercase AM/PM or localized period (e.g., "am" or "बिहान")
            - `A`: Uppercase AM/PM or localized period (e.g., "AM" or "साँझ")

        Example:
            >>> time = SimpleTime(hour=15, minute=30, second=45, nanosecond=123000000)
            >>> formatted_time = format_time_by_unicode_pattern(
            ...     time=time,
            ...     unicode_pattern="hh:mm:ss.SSS A",
            ...     language=language
            ... )
            >>> # formatted_time: "03:30:45.123 PM"
        """
        calendar_model = NepaliCalendarModel()
        return calendar_model.format_time_by_unicode_pattern(
            unicode_pattern=unicode_pattern,
            time=time,
            language=language
        )

    @staticmethod
    def format_english_date_by_unicode_pattern(
        unicode_pattern: str,
        calendar: CustomCalendar,
        language: NepaliCalendarUtilsLang = NepaliCalendarUtilsLang.ENGLISH
    ) -> str:
        """
        Formats an English date based on the specified Unicode pattern and language preferences.

        Args:
            unicode_pattern (str): A string specifying the pattern to use for formatting the date and time. 
                The pattern supports various placeholders like "yyyy", "MM", "dd", "D", "w", "E", etc.
            calendar (CustomCalendar): A custom calendar object representing the date.
            language (NepaliDatePickerLang): Specifies the language for formatting, including number and text localization.

        Returns:
            str: A string representing the formatted date according to the provided Unicode pattern and language preferences.

        Supported Unicode pattern placeholders:
            - `yyyy`: Four-digit year (e.g., "2025" or "२०२५")
            - `yy`: Two-digit year (e.g., "25" or "२५")
            - `MMMM`: Full month name (e.g., "January" or "जनवरी")
            - `MMM`: Abbreviated month name (e.g., "Jan" or "जन")
            - `MM`: Two-digit month (e.g., "01" or "०१")
            - `M`: Month number, no padding (e.g., "1" or "१")
            - `dd`: Two-digit day of the month (e.g., "04" or "०४")
            - `d`: Day of the month, no padding (e.g., "4" or "४")
            - `D`: Day of the year (1–366) (e.g., "123" or "१२३")
            - `w`: Week of the year (e.g., "23" or "२३")
            - `EEEE`: Full weekday name (e.g., "Monday" or "सोमबार")
            - `E`: Medium weekday name (e.g., "Mon" or "सोम")
            - `EEEEE`: Short weekday name, if defined (e.g., "M" or "स")
            - `ee`: Two-digit day of the week (e.g., "02" or "०२")
            - `e`: Day of the week, no padding (e.g., "2" or "२")

        Example:
            >>> calendar = CustomCalendar(year=2025, month=5, day_of_month=14, day_of_week=3, ...)
            >>> formatted_date = format_english_date_by_unicode_pattern(
            ...     "yyyy-MM-dd EEEE",
            ...     calendar,
            ...     language=NepaliDatePickerLang.ENGLISH
            ... )
            >>> # formatted_date: "2025-05-14 Tuesday"
        """
        calendar_model = NepaliCalendarModel()
        return calendar_model.format_english_date_by_unicode_pattern(
            unicode_pattern=unicode_pattern,
            calendar=calendar,
            language=language
        )

    @staticmethod
    def format_nepali_date_by_unicode_pattern(
        unicode_pattern: str,
        calendar: CustomCalendar,
        language: NepaliCalendarModel = NepaliCalendarUtilsLang.NEPALI
    ) -> str:
        """
        Formats a Nepali date based on the specified Unicode pattern and language preferences.

        Args:
            unicode_pattern (str): A string specifying the pattern to use for formatting the date and time.
                The pattern supports various placeholders like "yyyy", "MM", "dd", "D", "E", "ee", etc.
            calendar (CustomCalendar): A custom calendar object representing the Nepali date.
            language (NepaliDatePickerLang, optional): Language preference for formatting.
                Defaults to NepaliDatePickerLang.NEPALI, which uses Nepali names for months and weekdays.

        Returns:
            str: A string representing the formatted date and time according to the specified Unicode pattern and language.

        Supported Unicode pattern placeholders:
            - `yyyy`: Four-digit year (e.g., "2025" or "२०२५")
            - `yy`: Two-digit year (e.g., "25" or "२५")
            - `MMMM`: Full month name (e.g., "Baisakh" or "बैशाख")
            - `MMM`: Abbreviated month name (e.g., "Bai" or "बै")
            - `MM`: Two-digit month (e.g., "01" or "०१")
            - `M`: Month number, no padding (e.g., "1" or "१")
            - `dd`: Two-digit day of the month (e.g., "04" or "०४")
            - `d`: Day of the month, no padding (e.g., "4" or "४")
            - `D`: Day of the year (1–366) (e.g., "123" or "१२३")
            - `w`: Week of the year (e.g., "23" or "२३")
            - `EEEE`: Full weekday name (e.g., "Monday" or "सोमबार")
            - `E`: Medium weekday name (e.g., "Mon" or "सोम")
            - `EEEEE`: Short weekday name, if defined (e.g., "M" or "स")
            - `ee`: Two-digit day of the week (e.g., "02" or "०२")
            - `e`: Day of the week, no padding (e.g., "2" or "२")

        Example:
            >>> calendar = CustomCalendar(year=2025, month=5, day_of_month=14, day_of_week=3, ...)
            >>> formatted_date = format_nepali_date_by_unicode_pattern(
            ...     "yyyy-MM-dd EEEE",
            ...     calendar,
            ...     language=NepaliDatePickerLang.ENGLISH
            ... )
            >>> # formatted_date: "2025-05-14 Tuesday"
        """
        calendar_model = NepaliCalendarModel()
        return calendar_model.format_nepali_date_by_unicode_pattern(
            unicode_pattern=unicode_pattern,
            calendar=calendar,
            language=language
        )

    @staticmethod
    def format_english_date_time_by_unicode_pattern(
        unicode_pattern: str,
        calendar: CustomCalendar,
        time: SimpleTime = None,
        language: NepaliCalendarUtilsLang = NepaliCalendarUtilsLang.ENGLISH
    ) -> str:
        """
        Formats an English date and time based on the specified Unicode pattern and language preferences.

        Args:
            unicode_pattern (str): A string specifying the pattern to use for formatting the date and time.
                The pattern supports placeholders like "yyyy", "MM", "dd", "hh", "mm", "ss", etc.
            calendar (CustomCalendar): A custom calendar object representing the date.
            time (SimpleTime, optional): Time information (hour, minute, second, nanosecond).
                If omitted, the formatted string includes only the date.
            language (NepaliDatePickerLang, optional): Language preference for formatting.
                Defaults to NepaliDatePickerLang.ENGLISH, which uses English month and weekday names.

        Returns:
            str: A string representing the formatted date and time based on the Unicode pattern and language.

        Supported Unicode pattern placeholders:
            Date:
                - `yyyy`: Four-digit year (e.g., "2025" or "२०२५")
                - `yy`: Two-digit year (e.g., "25" or "२५")
                - `MMMM`: Full month name (e.g., "January" or "जनवरी")
                - `MMM`: Abbreviated month name (e.g., "Jan" or "जन")
                - `MM`: Two-digit month (e.g., "01" or "०१")
                - `M`: Month number, no padding (e.g., "1" or "१")
                - `dd`: Two-digit day of the month (e.g., "04" or "०४")
                - `d`: Day of the month, no padding (e.g., "4" or "४")
                - `D`: Day of the year (1–366) (e.g., "123" or "१२३")
                - `w`: Week of the year (e.g., "23" or "२३")
                - `EEEE`: Full weekday name (e.g., "Monday" or "सोमबार")
                - `E`: Medium weekday name (e.g., "Mon" or "सोम")
                - `EEEEE`: Short weekday name, if defined (e.g., "M" or "स")
                - `ee`: Two-digit day of week (e.g., "02" or "०२")
                - `e`: Day of week, no padding (e.g., "2" or "२")

            Time:
                - `HH`: Hour in 24-hour format (00–23) (e.g., "08" or "०८")
                - `H`: Hour in 24-hour format, no padding (e.g., "8" or "८")
                - `hh`: Hour in 12-hour format (01–12) (e.g., "01" or "०१")
                - `h`: Hour in 12-hour format, no padding (e.g., "1" or "१")
                - `mm`: Minutes, two-digit (e.g., "05" or "०५")
                - `m`: Minutes, no padding (e.g., "5" or "५")
                - `ss`: Seconds, two-digit (e.g., "09" or "०९")
                - `s`: Seconds, no padding (e.g., "9" or "९")
                - `SSSS`: Nanosecond precision (four digits, e.g., "1234" or "१२३४")
                - `SSS`: Milliseconds (e.g., "123" or "१२३")
                - `SS`: Two-digit fractional seconds (e.g., "12" or "१२")
                - `S`: One-digit fractional second (e.g., "1" or "१")

            Period:
                - `a`: Lowercase AM/PM or localized form (e.g., "am" or "बिहान")
                - `A`: Uppercase AM/PM or localized form (e.g., "AM" or "साँझ")

        Example:
            >>> calendar = CustomCalendar(year=2025, month=5, day_of_month=14, day_of_week=3, ...)
        >>> time = SimpleTime(hour=15, minute=30, second=45, nanosecond=123)
        >>> formatted = format_english_date_time_by_unicode_pattern(
        ...     "yyyy-MM-dd EEEE hh:mm:ss a",
        ...     calendar,
        ...     time
        ... )
        >>> # formatted: "2025-05-14 Tuesday 03:30:45 PM"
    """
        calendar_model = NepaliCalendarModel()
        return calendar_model.format_english_datetime_by_unicode_pattern(
            unicode_pattern=unicode_pattern,
            calendar=calendar,
            time=time,
            language=language
        )

    @staticmethod
    def format_nepali_date_time_by_unicode_pattern(
        unicode_pattern: str,
        calendar: CustomCalendar,
        time: SimpleTime = None,
        language: NepaliCalendarUtilsLang = NepaliCalendarUtilsLang.NEPALI
    ) -> str:
        """
        Formats a Nepali date and optional time using a Unicode-like pattern and language preferences.

        Args:
            calendar (CustomCalendar): A Nepali calendar date to format.
            time (SimpleTime, optional): Optional time with hour, minute, second, and nanosecond.
                                        If not provided, only the date is included in the output.
            unicode_pattern (str): A formatting pattern string using placeholders like "yyyy", "MM", "dd", "hh", "mm", etc.
            language (NepaliDatePickerLang, optional): Language used to localize names like months and weekdays.
                                            Defaults to NepaliDatePickerLang.NEPALI.

        Returns:
            str: A formatted date/time string based on the provided pattern and localization.

        Supported placeholders in `unicode_pattern`:

        Date:
            - yyyy: Four-digit year (e.g., "2025" or "२०२५")
            - yy: Two-digit year (e.g., "25" or "२५")
            - MMMM: Full month name (e.g., "Baisakh" or "बैशाख")
            - MMM: Abbreviated month name (e.g., "Bai" or "बै")
            - MM: Two-digit month (e.g., "01" or "०१")
            - M: Month without padding (e.g., "1" or "१")
            - dd: Two-digit day of month (e.g., "04" or "०४")
            - d: Day without padding (e.g., "4" or "४")
            - D: Day of year (1–366) (e.g., "123" or "१२३")
            - w: Week of year (e.g., "23" or "२३")

        Weekdays:
            - EEEE: Full weekday name (e.g., "Monday" or "सोमबार")
            - E: Medium weekday name (e.g., "Mon" or "सो")
            - EEEEE: Shortest weekday (e.g., "M" or "स")
            - ee: Two-digit day of week (e.g., "02" or "०२")
            - e: Day of week without padding (e.g., "2" or "२")

        Time:
            - HH: 24-hour format, two digits (e.g., "08" or "०८")
            - H: 24-hour format, no padding (e.g., "8" or "८")
            - hh: 12-hour format, two digits (e.g., "01" or "०१")
            - h: 12-hour format, no padding (e.g., "1" or "१")
            - mm: Minutes, two digits (e.g., "05" or "०५")
            - m: Minutes, no padding (e.g., "5" or "५")
            - ss: Seconds, two digits (e.g., "09" or "०९")
            - s: Seconds, no padding (e.g., "9" or "९")

        Fractions:
            - SSSS: Nanosecond precision (4 digits, e.g., "1234" or "१२३४")
            - SSS: Millisecond precision (e.g., "123" or "१२३")
            - SS: Hundredths (e.g., "12" or "१२")
            - S: Tenths (e.g., "1" or "१")

        Periods:
            - a: Lowercase period (e.g., "am" or "बिहान")
            - A: Uppercase period (e.g., "AM" or "साँझ")

        Example:
            >>> calendar = CustomCalendar(year=2025, month=5, day_of_month=14, day_of_week=3)
            >>> time = SimpleTime(hour=15, minute=30, second=45, nanosecond=123_000_000)
            >>> format_nepali_datetime_by_unicode_pattern(
            ...     calendar,
            ...     time,
            ...     "yyyy-MM-dd EEEE hh:mm:ss.SSS a",
            ...     language=NepaliDatePickerLang.ENGLISH
            ... )
            '2025-05-14 Tuesday 03:30:45.123 PM'
        """
        calendar_model = NepaliCalendarModel()
        return calendar_model.format_nepali_datetime_by_unicode_pattern(
            unicode_pattern=unicode_pattern,
            calendar=calendar,
            time=time,
            language=language
        )

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