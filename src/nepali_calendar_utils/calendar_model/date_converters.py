from typing import Tuple
from nepali_calendar_utils.calendar_model.nepali_calendar_defaults import *
from nepali_calendar_utils.data.nepali_year_month_map import *
from nepali_calendar_utils.data.custom_calendar import *
from datetime import date

class DateConverters:
    min_nepali_year = NepaliCalendarDefaults.NepaliYearRange[0]
    max_nepali_year = NepaliCalendarDefaults.NepaliYearRange[-1]
    min_english_year = NepaliCalendarDefaults.EnglishYearRange[0]
    max_english_year = NepaliCalendarDefaults.EnglishYearRange[-1]

    @staticmethod
    def get_total_days_in_nepali_month(nepaliYYYY: int, nepaliMM: int) -> int:
        return days_in_month_map[nepaliYYYY][nepaliMM]

    @staticmethod
    def convert_to_nepali_calendar(englishYYYY: int, englishMM: int, englishDD: int) -> CustomCalendar:
        if not DateConverters.is_english_date_in_conversion_range(englishYYYY, englishMM, englishDD):
            raise ValueError(f"Out of Range: English year {englishYYYY} is out of range to convert.")

        starting_english_date, starting_nepali_calendar = DateConverters.initialize_starting_dates(
            englishYYYY, False
        )

        english_base_date = date(
            year=starting_english_date.year,
            month=starting_english_date.month,
            day=starting_english_date.day_of_month
        )

        target_english_date = date(
            year=englishYYYY,
            month=englishMM,
            day=englishDD
        )

        total_days_difference = (target_english_date - english_base_date).days

        nepaliYYYY, nepaliMM, nepaliDD = (
            starting_nepali_calendar.year,
            starting_nepali_calendar.month,
            starting_nepali_calendar.day_of_month
        )
        day_of_week = starting_nepali_calendar.day_of_week

        day_of_year = starting_nepali_calendar.day_of_year
        week_of_year = starting_nepali_calendar.week_of_year
        week_of_month = starting_nepali_calendar.week_of_month

        first_day_of_month = starting_nepali_calendar.first_day_of_month
        last_day_of_month = starting_nepali_calendar.last_day_of_month

        total_days_in_month = days_in_month_map[nepaliYYYY][nepaliMM]

        for _ in range(total_days_difference):
            nepaliDD += 1
            day_of_year += 1
            day_of_week += 1
            
            if day_of_week > 7:
                day_of_week = 1
                week_of_year += 1
                week_of_month += 1

            if nepaliDD > total_days_in_month:
                nepaliMM += 1
                nepaliDD = 1

                if nepaliMM > 12:
                    nepaliYYYY += 1
                    nepaliMM = 1
                    day_of_year = 1
                    week_of_year = 1

                week_of_month = 1
                total_days_in_month = days_in_month_map[nepaliYYYY][nepaliMM]
                first_day_of_month = day_of_week

            remaining_days = total_days_in_month - nepaliDD
            last_day_of_month = (day_of_week + remaining_days) % 7 or 7

        return CustomCalendar(
            year=nepaliYYYY,
            month=nepaliMM,
            day_of_month=nepaliDD,
            day_of_week_in_month=(nepaliDD - 1) // 7 + 1,
            day_of_week=day_of_week,
            week_of_year=week_of_year,
            week_of_month=week_of_month,
            day_of_year=day_of_year,
            first_day_of_month=first_day_of_month,
            last_day_of_month=last_day_of_month,
            total_days_in_month=total_days_in_month,
            era=2
        )
        
    @staticmethod
    def convert_to_english_calendar(nepali_yyyy: int, nepali_mm: int, nepali_dd: int) -> CustomCalendar:
        if not DateConverters.is_nepali_calendar_in_conversion_range(nepali_yyyy, nepali_mm, nepali_dd):
            raise ValueError(f"Out of Range: Nepali year {nepali_yyyy} is out of range to convert.")

        starting_english_date, starting_nepali_calendar = DateConverters.initialize_starting_dates(nepali_yyyy, True)

        total_nep_days_count = DateConverters.calculate_total_nepali_days_count(
            starting_nepali_calendar, nepali_yyyy, nepali_mm, nepali_dd
        )

        english_yyyy, english_mm, english_dd = (
            starting_english_date.year,
            starting_english_date.month,
            starting_english_date.day_of_month,
        )

        day_of_week = starting_english_date.day_of_week
        day_of_year = starting_english_date.day_of_year
        week_of_year = starting_english_date.week_of_year
        week_of_month = starting_english_date.week_of_month

        first_day_of_month = starting_english_date.first_day_of_month
        last_day_of_month = starting_english_date.last_day_of_month

        total_days_in_month = DateConverters.get_total_days_in_english_month(english_yyyy, english_mm)

        for _ in range(total_nep_days_count):
            english_dd += 1
            day_of_week += 1
            day_of_year += 1

            if day_of_week > 7:
                day_of_week = 1
                week_of_year += 1
                week_of_month += 1

            if english_dd > total_days_in_month:
                english_mm += 1
                english_dd = 1
                week_of_month = 1

                if english_mm > 12:
                    english_yyyy += 1
                    english_mm = 1
                    day_of_year = 1
                    week_of_year = 1

                total_days_in_month = DateConverters.get_total_days_in_english_month(english_yyyy, english_mm)
                first_day_of_month = day_of_week

            remaining_days_of_the_month = total_days_in_month - english_dd
            last_day_of_month = (day_of_week + remaining_days_of_the_month) % 7

            if last_day_of_month == 0:
                last_day_of_month = 7

        return CustomCalendar(
            year=english_yyyy,
            month=english_mm,
            day_of_month=english_dd,
            first_day_of_month=first_day_of_month,
            last_day_of_month=last_day_of_month,
            day_of_week=day_of_week,
            day_of_week_in_month=(english_dd - 1) // 7 + 1,
            day_of_year=day_of_year,
            week_of_month=week_of_month,
            week_of_year=week_of_year,
            total_days_in_month=total_days_in_month,
            era=1,  # For English Date, the era is always 1 (for this library)
        )

     
    @staticmethod   
    def initialize_starting_dates(target_year: int, is_nepali_date: bool) -> tuple:
        reference_date = (
            nepali_date_map.get(target_year - 1)
            if is_nepali_date
            else english_date_map.get(target_year - 1)
        )

        starting_english_date = (
            reference_date.englishDate
            if reference_date and reference_date.englishDate
            else NepaliCalendarDefaults.startingEnglishCalendar
        )
        starting_nepali_calendar = (
            reference_date.nepaliDate
            if reference_date and reference_date.nepaliDate
            else NepaliCalendarDefaults.startingNepaliCalendar
        )

        return starting_english_date, starting_nepali_calendar

    @staticmethod
    def calculate_english_days_difference(starting_date: date, target_date: date) -> int:
        return (target_date - starting_date).days
    

    @staticmethod
    def calculate_total_nepali_days_count(
        starting_nepali_calendar: CustomCalendar, nepali_yyyy: int, nepali_mm: int, nepali_dd: int
    ) -> int:
        total_nep_days_count = 0

        for year in range(starting_nepali_calendar.year, nepali_yyyy):
            days_in_year = days_in_month_map[year]
            for month in range(1, 13):
                total_nep_days_count += days_in_year[month]

        for month in range(starting_nepali_calendar.month, nepali_mm):
            total_nep_days_count += days_in_month_map[nepali_yyyy][month]

        total_nep_days_count += nepali_dd - starting_nepali_calendar.day_of_month

        return total_nep_days_count

    @staticmethod
    def get_nepali_month(nepali_year: int, nepali_month: int, added_months_count: int) -> NepaliMonthCalendar:
        new_year, new_month = DateConverters.adjust_year_and_month(nepali_year, nepali_month + added_months_count)

        return DateConverters.calculate_nepali_month_details(new_year, new_month)

    @staticmethod
    def get_nepali_calendar(simple_nepali_date: SimpleDate) -> CustomCalendar:
        return DateConverters.get_custom_calendar_using_day_month_year(
            day_of_month=simple_nepali_date.day_of_month,
            month=simple_nepali_date.month,
            year=simple_nepali_date.year,
            adjust_month=False
        )
        
    # @staticmethod
    # def calculate_nepali_month_details(year: int, month: int) -> CustomCalendar:
    #     total_days_in_month = days_in_month_map.get(year, {}).get(month)
    #     print("My test mapper " + total_days_in_month)
    #     if total_days_in_month is None:
    #         raise ValueError(f"Invalid year {year} or month {month}.")

    #     starting_nepali_calendar = nepali_date_map.get(year - 1, None)
    #     print("My test mapper " + starting_nepali_calendar)
    #     if not starting_nepali_calendar:
    #         raise ValueError("Starting calendar not defined.")

    #     day_offset = DateConverters.calculate_day_offset(starting_nepali_calendar.year, year, month)
    #     first_day_of_month = (starting_nepali_calendar.first_day_of_month + day_offset) % 7
    #     normalized_first_day_of_month = 7 if first_day_of_month == 0 else first_day_of_month
    #     normalized_last_day_of_month = (
    #         (normalized_first_day_of_month + total_days_in_month - 1) % 7 or 7
    #     )

    #     return CustomCalendar(
    #         year=year,
    #         month=month,
    #         day_of_month=0,
    #         total_days_in_month=total_days_in_month,
    #         first_day_of_month=normalized_first_day_of_month,
    #         last_day_of_month=normalized_last_day_of_month,
    #         day_of_week_in_month=0,
    #         day_of_week=0,
    #         era=2,
    #         day_of_year=0,
    #         week_of_month=0,
    #         week_of_year=0,
    #     )

    @staticmethod
    def nepali_days_in_between(start_date: SimpleDate, end_date: SimpleDate) -> int:
        if start_date.year > end_date.year:
            return -DateConverters.nepali_days_in_between(end_date, start_date)

        if not (
            DateConverters.is_nepali_calendar_in_conversion_range(
                start_date.year, start_date.month, start_date.day_of_month
            )
            and DateConverters.is_nepali_calendar_in_conversion_range(
                end_date.year, end_date.month, end_date.day_of_month
            )
        ):
            raise ValueError(
                f"Out of range: Start year {start_date.year} or end year {end_date.year}."
            )

        start_offset = DateConverters.calculate_day_offset(start_date.year, start_date.year, start_date.month) + start_date.day_of_month
        end_offset = DateConverters.calculate_day_offset(start_date.year, end_date.year, end_date.month) + end_date.day_of_month

        return end_offset - start_offset

    @staticmethod
    def get_custom_calendar_using_day_month_year(year: int, month: int, day_of_month: int, adjust_month: bool) -> CustomCalendar:
        month_details = DateConverters.calculate_nepali_month_details(year, month)

        if adjust_month:
            new_day_of_month = min(day_of_month, month_details.total_days_in_month)
        else:
            if day_of_month > month_details.total_days_in_month:
                raise ValueError(f"Day {day_of_month} is out of range for month {month}.")
            new_day_of_month = day_of_month

        normalized_day_of_week = 7 if (month_details.first_day_of_month + new_day_of_month - 1) % 7 == 0 else (month_details.first_day_of_month + new_day_of_month - 1) % 7
        total_day_of_year = DateConverters.calculate_day_of_year(year, month, new_day_of_month)

        return CustomCalendar(
            year=year,
            month=month,
            day_of_month=new_day_of_month,
            total_days_in_month=month_details.total_days_in_month,
            first_day_of_month=month_details.first_day_of_month,
            last_day_of_month=month_details.last_day_of_month,
            day_of_week_in_month=(new_day_of_month - 1) // 7 + 1,
            day_of_week=normalized_day_of_week,
            era=2,
            day_of_year=total_day_of_year,
            week_of_month=DateConverters.calculate_week_of_month(
                day_of_month=day_of_month,
                first_day_of_month=month_details.first_day_of_month,
            ),
            week_of_year=DateConverters.calculate_week_of_year(
                total_day_of_year,
                DateConverters.calculate_nepali_month_details(year, 1).first_day_of_month,
            )
        )

    @staticmethod
    def adjust_nepali_date_for_day_adjustments(year: int, month: int, day_of_month: int, days_to_adjust: int) -> CustomCalendar:
        total_days_in_current_month = (
            days_in_month_map.get(year, [None])[month]
            if 1 <= month < len(days_in_month_map.get(year, [None]))
            else None
        )
        if total_days_in_current_month is None:
            raise ValueError(f"Invalid year {year} or month {month}.")

        if 1 <= day_of_month + days_to_adjust <= total_days_in_current_month:
            new_day = day_of_month + days_to_adjust
            return DateConverters.get_custom_calendar_using_day_month_year(year, month, new_day, True)

        if days_to_adjust > 0:
            remaining_days = days_to_adjust - (total_days_in_current_month - day_of_month + 1)
            new_month = month + 1
            new_year = year + 1 if new_month > 12 else year
            return DateConverters.adjust_nepali_date_for_day_adjustments(
                new_year, 1 if new_month > 12 else new_month, 1, remaining_days
            )
        else:
            new_month = month - 1
            new_year = year - 1 if new_month < 1 else year
            previous_month_days = days_in_month_map.get(new_year, [])[12 if new_month < 1 else new_month]

            if previous_month_days == 0:
                raise ValueError(f"Invalid year {new_year} or month {new_month}.")

            return DateConverters.adjust_nepali_date_for_day_adjustments(
                new_year,
                12 if new_month < 1 else new_month,
                previous_month_days,
                days_to_adjust + day_of_month,
            )
    
    @staticmethod
    def adjust_year_and_month(year: int, month: int) -> Tuple[int, int]:
        adjusted_year = year
        adjusted_month = month

        # Handle month overflow
        while adjusted_month > 12:
            adjusted_month -= 12
            adjusted_year += 1

        # Handle month underflow
        while adjusted_month < 1:
            adjusted_month += 12
            adjusted_year -= 1

        return adjusted_year, adjusted_month

    @staticmethod
    def calculate_nepali_month_details(nepali_year: int, nepali_month: int) -> NepaliMonthCalendar:

        if nepali_year not in days_in_month_map or nepali_month not in range(1, 13):
            raise ValueError(f"Invalid year {nepali_year} or month provided {nepali_month}.")
        
        total_days_in_month = days_in_month_map[nepali_year][nepali_month]

        starting_nepali_calendar = (
            nepali_date_map.get(nepali_year - 1, {}).nepaliDate 
            if nepali_date_map.get(nepali_year - 1) else NepaliCalendarDefaults.startingNepaliCalendar
        )
        
        day_offset = DateConverters.calculate_day_offset(starting_nepali_calendar.year, nepali_year, nepali_month)

        first_day_of_month = (starting_nepali_calendar.first_day_of_month + day_offset) % 7
        normalized_first_day_of_month = 7 if first_day_of_month == 0 else first_day_of_month

        normalized_last_day_of_month = ((normalized_first_day_of_month + total_days_in_month - 1) % 7)
        normalized_last_day_of_month = 7 if normalized_last_day_of_month == 0 else normalized_last_day_of_month

        return NepaliMonthCalendar(
            year=nepali_year,
            month=nepali_month,
            first_day_of_month=normalized_first_day_of_month,
            total_days_in_month=total_days_in_month,
            last_day_of_month=normalized_last_day_of_month
        )

    @staticmethod
    def calculate_day_offset(starting_year: int, target_year: int, target_month: int) -> int:        
        for year in range(starting_year, target_year):
            if year not in days_in_month_map:
                raise ValueError(f"Year {year} is missing in days_in_month_map.")
        
        year_offset = sum(
            sum(days_in_month_map[year][1:])
            for year in range(starting_year, target_year)
        )
        
        if target_year in days_in_month_map:
            month_offset = sum(days_in_month_map[target_year][1:target_month])
        else:
            raise ValueError(f"Target year {target_year} is missing in days_in_month_map.")
        
        return year_offset + month_offset

    @staticmethod
    def calculate_day_of_year(year: int, month: int, day_of_month: int) -> int:
        if year not in days_in_month_map:
            raise ValueError(f"Year {year} is not present in the days_in_month_map.")
        
        days_in_year = days_in_month_map[year]
        month_offset = sum(days_in_year[1:month])

        return month_offset + day_of_month

    @staticmethod
    def calculate_week_of_month(day_of_month: int, first_day_of_month: int) -> int:
        days_before = (day_of_month - 1) + (first_day_of_month - 1)
        return (days_before // 7) + 1

    @staticmethod
    def calculate_week_of_year(day_of_year: int, first_day_of_year: int) -> int:
        total_days_passed = day_of_year + (first_day_of_year - 1)
        return (total_days_passed // 7) + (1 if total_days_passed % 7 != 0 else 0)
    
    @staticmethod
    def get_total_days_in_english_month(year: int, month: int) -> int:
        if not (1 <= month <= 12):
            raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")
        
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days_in_month_of_leap_year = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if DateConverters.is_english_leap_year(year):
            return days_in_month_of_leap_year[month]
        return days_in_month[month]

    @staticmethod
    def is_nepali_calendar_in_conversion_range(nepali_yyyy: int, nepali_mm: int, nepali_dd: int) -> bool:
        return (
            DateConverters.min_nepali_year <= nepali_yyyy <= DateConverters.max_nepali_year
            and 1 <= nepali_mm <= 12
            and 1 <= nepali_dd <= 32
        )
        
    @staticmethod
    def is_english_date_in_conversion_range(english_yyyy: int, english_mm: int, english_dd: int) -> bool:
        return (
            DateConverters.min_english_year <= english_yyyy <= DateConverters.max_english_year
            and 1 <= english_mm <= 12
            and 1 <= english_dd <= 31
        )

    @staticmethod
    def is_english_leap_year(year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)