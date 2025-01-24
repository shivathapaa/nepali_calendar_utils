import unittest
from nepali_calendar_utils.data.custom_calendar import *
from nepali_calendar_utils.calendar_model.nepali_calendar_model import NepaliCalendarModel
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.nepali_date_locale import NameFormat, NepaliDateFormatStyle, NepaliDateLocale, NepaliDatePickerLang

class TestNepaliDateConverter(unittest.TestCase):
    def setUp(self):
        self.calendar_model = NepaliCalendarModel()
        
    def test_nepali_to_english_date_converter_nepali_new_year_2079(self):
        converter = NepaliDateConverter()
        
        to_test_english_calendar = converter.convert_nepali_to_english(
            nepali_yyyy=2079, nepali_mm=1, nepali_dd=1
        )

        correct_english_custom_calendar = CustomCalendar(
            year=2022,
            month=4,
            day_of_month=14,
            era=1,
            first_day_of_month=6,
            last_day_of_month=7,
            total_days_in_month=30,
            day_of_week_in_month=2,
            day_of_week=5,
            day_of_year=104,
            week_of_month=3,
            week_of_year=16
        )

        self.assertEqual(correct_english_custom_calendar, to_test_english_calendar)

    def test_nepali_to_english_date_converter_nepali_new_year_2082(self):
        to_test_english_calendar = NepaliDateConverter.convert_nepali_to_english(
            nepali_yyyy=2082, nepali_mm=1, nepali_dd=1
        )

        correct_english_custom_calendar = CustomCalendar(
            year=2025,
            month=4,
            day_of_month=14,
            era=1,
            first_day_of_month=3,
            last_day_of_month=4,
            total_days_in_month=30,
            day_of_week_in_month=2,
            day_of_week=2,
            day_of_year=104,
            week_of_month=3,
            week_of_year=16
        )

        self.assertEqual(correct_english_custom_calendar, to_test_english_calendar)

    def test_nepali_to_english_date_converter_nepali_year_2100_11_12(self):
        to_test_english_calendar = NepaliDateConverter.convert_nepali_to_english(
            nepali_yyyy=2100, nepali_mm=11, nepali_dd=12
        )

        correct_english_custom_calendar = CustomCalendar(
            year=2044,
            month=2,
            day_of_month=24,
            era=1,
            first_day_of_month=2,
            last_day_of_month=2,
            total_days_in_month=29,
            day_of_week_in_month=4,
            day_of_week=4,
            day_of_year=55,
            week_of_month=4,
            week_of_year=9
        )

        self.assertEqual(correct_english_custom_calendar, to_test_english_calendar)

    def test_nepali_to_english_date_converter_nepali_year_2087_9_21(self):
        to_test_english_calendar = NepaliDateConverter.convert_nepali_to_english(
            nepali_yyyy=2087, nepali_mm=9, nepali_dd=21
        )

        correct_english_custom_calendar = CustomCalendar(
            year=2031,
            month=1,
            day_of_month=5,
            era=1,
            first_day_of_month=4,
            last_day_of_month=6,
            total_days_in_month=31,
            day_of_week_in_month=1,
            day_of_week=1,
            day_of_year=5,
            week_of_month=2,
            week_of_year=2
        )

        self.assertEqual(correct_english_custom_calendar, to_test_english_calendar)

    def test_nepali_to_english_date_converter_nepali_year_2097_3_17(self):
        to_test_english_calendar = NepaliDateConverter.convert_nepali_to_english(
            nepali_yyyy=2097, nepali_mm=3, nepali_dd=17
        )

        correct_english_custom_calendar = CustomCalendar(
            year=2040,
            month=7,
            day_of_month=1,
            era=1,
            first_day_of_month=1,
            last_day_of_month=3,
            total_days_in_month=31,
            day_of_week_in_month=1,
            day_of_week=1,
            day_of_year=183,
            week_of_month=1,
            week_of_year=27
        )

        self.assertEqual(correct_english_custom_calendar, to_test_english_calendar)

    def test_nepali_to_english_date_converter_nepali_year_2034_6_29(self):
        to_test_english_calendar = NepaliDateConverter.convert_nepali_to_english(
            nepali_yyyy=2034, nepali_mm=6, nepali_dd=29
        )

        correct_english_custom_calendar = CustomCalendar(
            year=1977,
            month=10,
            day_of_month=15,
            era=1,
            first_day_of_month=7,
            last_day_of_month=2,
            total_days_in_month=31,
            day_of_week_in_month=3,
            day_of_week=7,
            day_of_year=288,
            week_of_month=3,
            week_of_year=42
        )

        self.assertEqual(correct_english_custom_calendar, to_test_english_calendar)

    def test_english_to_nepali_date_converter_english_year_2000_6_24(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2000, english_mm=6, english_dd=24
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2057,
            month=3,
            day_of_month=10,
            era=2,
            first_day_of_month=5,
            last_day_of_month=7,
            total_days_in_month=31,
            day_of_week_in_month=2,
            day_of_week=7,
            day_of_year=73,
            week_of_month=2,
            week_of_year=11
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)


    def test_english_to_nepali_date_converter_english_year_19770513(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=1997, english_mm=5, english_dd=13
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2054,
            month=1,
            day_of_month=31,
            era=2,
            first_day_of_month=1,
            last_day_of_month=3,
            total_days_in_month=31,
            day_of_week_in_month=5,
            day_of_week=3,
            day_of_year=31,
            week_of_month=5,
            week_of_year=5
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_english_to_nepali_date_converter_english_year_19140808(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=1914, english_mm=8, english_dd=8
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=1971,
            month=4,
            day_of_month=24,
            era=2,
            first_day_of_month=5,
            last_day_of_month=7,
            total_days_in_month=31,
            day_of_week_in_month=4,
            day_of_week=7,
            day_of_year=118,
            week_of_month=4,
            week_of_year=17
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_english_to_nepali_date_converter_english_year_20250615(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2025, english_mm=6, english_dd=15
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2082,
            month=3,
            day_of_month=1,
            era=2,
            first_day_of_month=1,
            last_day_of_month=3,
            total_days_in_month=31,
            day_of_week_in_month=1,
            day_of_week=1,
            day_of_year=63,
            week_of_month=1,
            week_of_year=10
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_english_to_nepali_date_converter_english_leap_year_20240229(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2024, english_mm=2, english_dd=29
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2080,
            month=11,
            day_of_month=17,
            era=2,
            first_day_of_month=3,
            last_day_of_month=4,
            total_days_in_month=30,
            day_of_week_in_month=3,
            day_of_week=5,
            day_of_year=322,
            week_of_month=3,
            week_of_year=47
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_english_to_nepali_date_converter_english_year_20320605(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2032, english_mm=6, english_dd=5
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2089,
            month=2,
            day_of_month=23,
            era=2,
            first_day_of_month=6,
            last_day_of_month=2,
            total_days_in_month=32,
            day_of_week_in_month=4,
            day_of_week=7,
            day_of_year=53,
            week_of_month=4,
            week_of_year=8
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_english_to_nepali_date_converter_english_year_20431014_get_nepali_year_21000627(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2043, english_mm=10, english_dd=14
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2100,
            month=6,
            day_of_month=27,
            era=2,
            first_day_of_month=6,
            last_day_of_month=7,
            total_days_in_month=30,
            day_of_week_in_month=4,
            day_of_week=4,
            day_of_year=184,
            week_of_month=5,
            week_of_year=27
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    # Test for a year limit of 2043 (commented out to indicate behavior)
    # def test_english_to_nepali_date_converter_english_year_20440412_get_nepali_year_21001230(self):
    #     to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
    #         english_yyyy=2044, english_mm=4, english_dd=12
    #     )
    #
    #     correct_nepali_custom_calendar = CustomCalendar(
    #         year=2100,
    #         month=12,
    #         day_of_month=30,
    #         era=2,
    #         first_day_of_month=2,
    #         last_day_of_month=4,
    #         total_days_in_month=31,
    #         day_of_week_in_month=5,
    #         day_of_week=3,
    #         day_of_year=365,
    #         week_of_month=5,
    #         week_of_year=53
    #     )
    #
    #     self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_english_to_nepali_date_converter_english_after_leap_year_20240302_get_nepali_year_20801119(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2024, english_mm=3, english_dd=2
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2080,
            month=11,
            day_of_month=19,
            era=2,
            first_day_of_month=3,
            last_day_of_month=4,
            total_days_in_month=30,
            day_of_week_in_month=3,
            day_of_week=7,
            day_of_year=324,
            week_of_month=3,
            week_of_year=47
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_english_to_nepali_date_converter_english_after_leap_year_first_day_of_week_20240303_get_nepali_year_20801120(self):
        to_test_nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2024, english_mm=3, english_dd=3
        )

        correct_nepali_custom_calendar = CustomCalendar(
            year=2080,
            month=11,
            day_of_month=20,
            era=2,
            first_day_of_month=3,
            last_day_of_month=4,
            total_days_in_month=30,
            day_of_week_in_month=3,
            day_of_week=1,
            day_of_year=325,
            week_of_month=4,
            week_of_year=48
        )

        self.assertEqual(correct_nepali_custom_calendar, to_test_nepali_calendar)

    def test_date_conversion_convert_to_english_get_same_from_convert_to_nepali(self):
        nepali_calendar = NepaliDateConverter.convert_english_to_nepali(
            english_yyyy=2021, english_mm=2, english_dd=28
        )

        english_calendar = NepaliDateConverter.convert_nepali_to_english(
            nepali_yyyy=nepali_calendar.year,
            nepali_mm=nepali_calendar.month,
            nepali_dd=nepali_calendar.day_of_month
        )

        self.assertEqual(2021, english_calendar.year)
        self.assertEqual(2, english_calendar.month)
        self.assertEqual(28, english_calendar.day_of_month)
        

    def test_get_nepali_month_today_nepali_date_get_same_custom_month_and_nepali_calendar_properties(self):
        today = self.calendar_model.today_nepali_calendar

        nepali_month_from_simple_date = self.calendar_model.get_nepali_calendar(today.to_simple_date())
        nepali_month_from_year_and_month = self.calendar_model.get_nepali_month(
            nepali_year=today.year, nepali_month=today.month
        )

        self.assertEqual(today.to_nepali_month_calendar(), nepali_month_from_year_and_month)
        self.assertEqual(nepali_month_from_year_and_month, nepali_month_from_simple_date.to_nepali_month_calendar())

    def test_get_nepali_month_add_one_month_to_208203_get_nepali_calendar_of_date_208104(self):
        nepali_custom_calendar = CustomCalendar(
            year=2082, month=3, day_of_month=1, era=2,
            first_day_of_month=1, last_day_of_month=3, total_days_in_month=31,
            day_of_week_in_month=1, day_of_week=1, day_of_year=63,
            week_of_month=1, week_of_year=10
        )

        custom_calendar_after_one_month_added = self.calendar_model.plus_nepali_months(
            from_nepali_calendar=nepali_custom_calendar.to_nepali_month_calendar(), added_months_count=1
        )

        correct_custom_calendar_after_addition = CustomCalendar(
            year=2082, month=4, day_of_month=1, era=2,
            first_day_of_month=4, last_day_of_month=7, total_days_in_month=32,
            day_of_week_in_month=1, day_of_week=4, day_of_year=94,
            week_of_month=1, week_of_year=14
        )

        self.assertEqual(correct_custom_calendar_after_addition.year, custom_calendar_after_one_month_added.year)
        self.assertEqual(correct_custom_calendar_after_addition.month, custom_calendar_after_one_month_added.month)
        self.assertEqual(correct_custom_calendar_after_addition.first_day_of_month, custom_calendar_after_one_month_added.first_day_of_month)
        self.assertEqual(correct_custom_calendar_after_addition.last_day_of_month, custom_calendar_after_one_month_added.last_day_of_month)
        self.assertEqual(correct_custom_calendar_after_addition.total_days_in_month, custom_calendar_after_one_month_added.total_days_in_month)

    def test_calculate_positive_english_days_in_between(self):
        start_date = SimpleDate(2016, 2, 16)
        end_date = SimpleDate(2021, 3, 27)

        days_between = NepaliDateConverter.get_english_days_in_between(start_date, end_date)

        self.assertEqual(1866, days_between)

    def test_calculate_negative_english_days_in_between(self):
        start_date = SimpleDate(2024, 3, 8)
        end_date = SimpleDate(1980, 12, 31)

        days_between = NepaliDateConverter.get_english_days_in_between(start_date, end_date)

        self.assertEqual(-15773, days_between)

    def test_calculate_positive_nepali_days_in_between(self):
        start_date = SimpleDate(1980, 12, 31)
        end_date = SimpleDate(2081, 5, 24)

        days_between = NepaliDateConverter.get_nepali_days_in_between(start_date, end_date)

        self.assertEqual(36675, days_between)
        
        
    def test_get_nepali_month_today(self):
        today = self.calendar_model.today_nepali_calendar

        nepali_month_from_simple_date = self.calendar_model.get_nepali_calendar(
            simple_nepali_date=today.to_simple_date()
        )
        nepali_month_from_year_and_month = self.calendar_model.get_nepali_month(
            nepali_year=today.year, nepali_month=today.month
        )

        self.assertEqual(today.to_nepali_month_calendar(), nepali_month_from_year_and_month)
        self.assertEqual(
            nepali_month_from_year_and_month,
            nepali_month_from_simple_date.to_nepali_month_calendar()
        )

    def test_add_one_month(self):
        nepali_custom_calendar = CustomCalendar(
            year=2082, month=3, day_of_month=1, era=2,
            first_day_of_month=1, last_day_of_month=3,
            total_days_in_month=31, day_of_week_in_month=1,
            day_of_week=1, day_of_year=63, week_of_month=1,
            week_of_year=10
        )

        result = NepaliCalendarModel.plus_nepali_months(
            from_nepali_calendar=nepali_custom_calendar.to_nepali_month_calendar(),
            added_months_count=1
        )

        expected = CustomCalendar(
            year=2082, month=4, day_of_month=1, era=2,
            first_day_of_month=4, last_day_of_month=7,
            total_days_in_month=32, day_of_week_in_month=1,
            day_of_week=4, day_of_year=94, week_of_month=1,
            week_of_year=14
        )

        self.assertEqual(expected.year, result.year)
        self.assertEqual(expected.month, result.month)
        self.assertEqual(expected.first_day_of_month, result.first_day_of_month)
        self.assertEqual(expected.last_day_of_month, result.last_day_of_month)
        self.assertEqual(expected.total_days_in_month, result.total_days_in_month)

    def test_add_twenty_four_months(self):
        nepali_custom_calendar = CustomCalendar(
            year=2079, month=4, day_of_month=1, era=2,
            first_day_of_month=1, last_day_of_month=3,
            total_days_in_month=31, day_of_week_in_month=1,
            day_of_week=1, day_of_year=95, week_of_month=1,
            week_of_year=15
        )

        result = self.calendar_model.plus_nepali_months(
            from_nepali_calendar=nepali_custom_calendar.to_nepali_month_calendar(),
            added_months_count=24
        )

        expected = CustomCalendar(
            year=2081, month=4, day_of_month=1, era=2,
            first_day_of_month=3, last_day_of_month=6,
            total_days_in_month=32, day_of_week_in_month=1,
            day_of_week=3, day_of_year=95, week_of_month=1,
            week_of_year=15
        )

        self.assertEqual(expected.year, result.year)
        self.assertEqual(expected.month, result.month)
        self.assertEqual(expected.first_day_of_month, result.first_day_of_month)
        self.assertEqual(expected.last_day_of_month, result.last_day_of_month)
        self.assertEqual(expected.total_days_in_month, result.total_days_in_month)

    def test_subtract_four_months(self):
        nepali_custom_calendar = CustomCalendar(
            year=2082, month=4, day_of_month=1, era=2,
            first_day_of_month=4, last_day_of_month=7,
            total_days_in_month=32, day_of_week_in_month=1,
            day_of_week=4, day_of_year=94, week_of_month=1,
            week_of_year=14
        )

        result = self.calendar_model.minus_nepali_months(
            from_nepali_calendar=nepali_custom_calendar.to_nepali_month_calendar(),
            subtracted_months_count=4
        )

        expected = CustomCalendar(
            year=2081, month=12, day_of_month=1, era=2,
            first_day_of_month=6, last_day_of_month=1,
            total_days_in_month=31, day_of_week_in_month=1,
            day_of_week=6, day_of_year=336, week_of_month=1,
            week_of_year=49
        )

        self.assertEqual(expected.year, result.year)
        self.assertEqual(expected.month, result.month)
        self.assertEqual(expected.first_day_of_month, result.first_day_of_month)
        self.assertEqual(expected.last_day_of_month, result.last_day_of_month)
        self.assertEqual(expected.total_days_in_month, result.total_days_in_month)

    def test_calculate_first_and_last_day_of_month(self):
        custom_calendar_2079 = CustomCalendar(
            year=2079, month=4, day_of_month=1, era=2,
            first_day_of_month=1, last_day_of_month=3,
            total_days_in_month=31, day_of_week_in_month=1,
            day_of_week=1, day_of_year=95, week_of_month=1,
            week_of_year=15
        )

        custom_calendar_2082 = CustomCalendar(
            year=2082, month=4, day_of_month=1, era=2,
            first_day_of_month=4, last_day_of_month=7,
            total_days_in_month=32, day_of_week_in_month=1,
            day_of_week=4, day_of_year=94, week_of_month=1,
            week_of_year=14
        )

        result_2079 = NepaliDateConverter.get_nepali_month_calendar(
            nepali_year=custom_calendar_2079.year,
            nepali_month=custom_calendar_2079.month
        )
        result_2082 = NepaliDateConverter.get_nepali_month_calendar(
            nepali_year=custom_calendar_2082.year,
            nepali_month=custom_calendar_2082.month
        )

        self.assertEqual(custom_calendar_2079.year, result_2079.year)
        self.assertEqual(custom_calendar_2079.month, result_2079.month)
        self.assertEqual(custom_calendar_2079.first_day_of_month, result_2079.first_day_of_month)
        self.assertEqual(custom_calendar_2079.last_day_of_month, result_2079.last_day_of_month)
        self.assertEqual(custom_calendar_2079.total_days_in_month, result_2079.total_days_in_month)
        self.assertEqual(custom_calendar_2082.year, result_2082.year)
        self.assertEqual(custom_calendar_2082.month, result_2082.month)
        self.assertEqual(custom_calendar_2082.first_day_of_month, result_2082.first_day_of_month)
        self.assertEqual(custom_calendar_2082.last_day_of_month, result_2082.last_day_of_month)
        self.assertEqual(custom_calendar_2082.total_days_in_month, result_2082.total_days_in_month)


    def test_calculate_positive_english_days_in_between(self):
        start_date = SimpleDate(2016, 2, 16)
        end_date = SimpleDate(2021, 3, 27)

        days_between = NepaliDateConverter.get_english_days_in_between(start_date, end_date)

        self.assertEqual(days_between, 1866)

    def test_calculate_positive_english_days_in_between_v2(self):
        start_date = SimpleDate(1980, 12, 31)
        end_date = SimpleDate(2024, 3, 8)

        days_between = NepaliDateConverter.get_english_days_in_between(start_date, end_date)

        self.assertEqual(days_between, 15773)

    def test_calculate_negative_english_days_in_between(self):
        end_date = SimpleDate(1980, 12, 31)
        start_date = SimpleDate(2024, 3, 8)

        days_between = NepaliDateConverter.get_english_days_in_between(start_date, end_date)

        self.assertEqual(days_between, -15773)

    def test_calculate_positive_nepali_days_in_between(self):
        start_date = SimpleDate(1980, 12, 31)
        end_date = SimpleDate(2081, 5, 24)

        days_between = NepaliDateConverter.get_nepali_days_in_between(start_date, end_date)

        self.assertEqual(days_between, 36675)

    def test_calculate_negative_nepali_days_in_between(self):
        end_date = SimpleDate(1980, 12, 31)
        start_date = SimpleDate(2081, 5, 24)

        days_between = NepaliDateConverter.get_nepali_days_in_between(start_date, end_date)

        self.assertEqual(days_between, -36675)


    def test_compare_both_english_and_nepali_days_in_between(self):
        english_start_date = SimpleDate(1998, 4, 12)
        english_end_date = SimpleDate(2024, 9, 21)
        nepali_start_date = SimpleDate(2054, 12, 30)
        nepali_end_date = SimpleDate(2081, 6, 5)

        expected_days_difference = 9659

        nepali_days_between = NepaliDateConverter.get_nepali_days_in_between(nepali_start_date, nepali_end_date)
        english_days_between = NepaliDateConverter.get_english_days_in_between(english_start_date, english_end_date)

        self.assertEqual(expected_days_difference, nepali_days_between)
        self.assertEqual(expected_days_difference, english_days_between)
        self.assertEqual(nepali_days_between, english_days_between)

    def test_compare_calculated_nepali_calendar_using_day_month_year(self):
        converter = NepaliDateConverter()
        today = converter.today_nepali_calendar
        
        calculated_nepali_calendar_from_today = NepaliDateConverter.get_nepali_calendar(today.year, today.month, today.day_of_month)

        self.assertEqual(today, calculated_nepali_calendar_from_today)

        custom_start_calendar_of_2079 = CustomCalendar(
            year=2079,
            month=4,
            day_of_month=1,
            era=2,
            first_day_of_month=1,
            last_day_of_month=3,
            total_days_in_month=31,
            day_of_week_in_month=1,
            day_of_week=1,
            day_of_year=95,
            week_of_month=1,
            week_of_year=15
        )
        
        calculated_nepali_calendar_of_2079_start = NepaliDateConverter.get_nepali_calendar(
            custom_start_calendar_of_2079.year, custom_start_calendar_of_2079.month, custom_start_calendar_of_2079.day_of_month
        )

        self.assertEqual(custom_start_calendar_of_2079, calculated_nepali_calendar_of_2079_start)

        custom_start_calendar_of_2082 = CustomCalendar(
            year=2082,
            month=4,
            day_of_month=1,
            era=2,
            first_day_of_month=4,
            last_day_of_month=7,
            total_days_in_month=32,
            day_of_week_in_month=1,
            day_of_week=4,
            day_of_year=94,
            week_of_month=1,
            week_of_year=14
        )
        
        calculated_nepali_calendar_of_2082_start = NepaliDateConverter.get_nepali_calendar(
            custom_start_calendar_of_2082.year, custom_start_calendar_of_2082.month, custom_start_calendar_of_2082.day_of_month
        )

        self.assertEqual(custom_start_calendar_of_2082, calculated_nepali_calendar_of_2082_start)

        custom_end_calendar_of_2054 = CustomCalendar(
            year=2054,
            month=1,
            day_of_month=31,
            era=2,
            first_day_of_month=1,
            last_day_of_month=3,
            total_days_in_month=31,
            day_of_week_in_month=5,
            day_of_week=3,
            day_of_year=31,
            week_of_month=5,
            week_of_year=5
        )
        
        calculated_nepali_calendar_of_2054_end = NepaliDateConverter.get_nepali_calendar(
            custom_end_calendar_of_2054.year, custom_end_calendar_of_2054.month, custom_end_calendar_of_2054.day_of_month
        )

        self.assertEqual(custom_end_calendar_of_2054, calculated_nepali_calendar_of_2054_end)

    def test_compare_nepali_calendar_after_day_adjustments(self):
        converter = NepaliDateConverter()
        today = converter.today_nepali_calendar
        adjusted_calendar_of_today = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            today.year, today.month, today.day_of_month, 0
        )

        self.assertEqual(today, adjusted_calendar_of_today)

        custom_start_calendar_of_2082 = CustomCalendar(
            year=2082,
            month=4,
            day_of_month=1,
            era=2,
            first_day_of_month=4,
            last_day_of_month=7,
            total_days_in_month=32,
            day_of_week_in_month=1,
            day_of_week=4,
            day_of_year=94,
            week_of_month=1,
            week_of_year=14
        )

        adjusted_calendar_of_2082 = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(
            custom_start_calendar_of_2082.year, custom_start_calendar_of_2082.month, 20, -19
        )

        self.assertEqual(custom_start_calendar_of_2082, adjusted_calendar_of_2082)

        get_nepali_calendar_2081 = NepaliDateConverter.get_nepali_calendar(2081, 5, 28)
        adjusted_nepali_calendar_2081 = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2081, 6, 9, -12)

        self.assertEqual(get_nepali_calendar_2081, adjusted_nepali_calendar_2081)

        get_nepali_calendar_2084 = NepaliDateConverter.get_nepali_calendar(2084, 1, 2)
        adjusted_nepali_calendar_2083 = NepaliDateConverter.get_nepali_calendar_after_addition_or_subtraction(2083, 12, 25, 7)

        self.assertEqual(get_nepali_calendar_2084, adjusted_nepali_calendar_2083)

    def test_compare_end_week_day_specifically_for_get_nepali_calendar(self):
        nepali_calendar_for_end_weekday_using_english_date = NepaliDateConverter.convert_english_to_nepali(2024, 9, 28)
        nepali_calendar_for_end_weekday_using_nepali_date = NepaliDateConverter.get_nepali_calendar(2081, 6, 12)

        nepali_calendar_for_end_year_end_weekday_using_english_date = NepaliDateConverter.convert_english_to_nepali(2025, 4, 12)
        nepali_calendar_for_end_year_end_weekday_using_nepali_date = NepaliDateConverter.get_nepali_calendar(2081, 12, 30)

        self.assertEqual(nepali_calendar_for_end_weekday_using_english_date, nepali_calendar_for_end_weekday_using_nepali_date)
        self.assertEqual(nepali_calendar_for_end_year_end_weekday_using_english_date, nepali_calendar_for_end_year_end_weekday_using_nepali_date)

    def test_compare_start_week_day_specifically_for_get_nepali_calendar(self):
        nepali_calendar_for_start_weekday_using_english_date = NepaliDateConverter.convert_english_to_nepali(2024, 9, 29)
        nepali_calendar_for_start_weekday_using_nepali_date = NepaliDateConverter.get_nepali_calendar(2081, 6, 13)

        nepali_calendar_for_end_year_start_weekday_using_english_date = NepaliDateConverter.convert_english_to_nepali(2025, 4, 13)
        nepali_calendar_for_end_year_start_weekday_using_nepali_date = NepaliDateConverter.get_nepali_calendar(2081, 12, 31)

        self.assertEqual(nepali_calendar_for_start_weekday_using_english_date, nepali_calendar_for_start_weekday_using_nepali_date)
        self.assertEqual(nepali_calendar_for_end_year_start_weekday_using_english_date, nepali_calendar_for_end_year_start_weekday_using_nepali_date)

    def test_format_nepali_date_random_date_get_formatted_date_in_string_by_locale(self):
        english_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.ENGLISH,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.FULL,
            month_name=NameFormat.FULL
        )

        nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.MEDIUM,
            month_name=NameFormat.FULL
        )

        full_format_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.FULL,
            month_name=NameFormat.FULL
        )

        to_test_formatted_date_in_english = NepaliDateConverter.format_nepali_date(
            year=2080, month=3, day_of_month=15, day_of_week=3, locale=english_locale
        )
        formatted_date_in_english = "Tuesday, Asar 15, 2080"

        to_test_formatted_date_in_nepali = NepaliDateConverter.format_nepali_date(
            year=2080, month=6, day_of_month=2, day_of_week=5, locale=nepali_locale
        )
        formatted_date_in_nepali = "२०८० असोज २"

        to_test_full_formatted_date_in_nepali = NepaliDateConverter.format_nepali_date(
            year=2080, month=2, day_of_month=2, day_of_week=5, locale=full_format_nepali_locale
        )
        full_formatted_date_in_nepali = "बिहिबार, जेठ २, २०८०"

        self.assertEqual(formatted_date_in_english, to_test_formatted_date_in_english)
        self.assertEqual(formatted_date_in_nepali, to_test_formatted_date_in_nepali)
        self.assertEqual(full_formatted_date_in_nepali, to_test_full_formatted_date_in_nepali)

    def test_format_nepali_date_using_other_helper_function_of_names_custom_calendar_date_get_formatted_date_in_string(self):
        date_converter = NepaliDateConverter()
        custom_calendar = date_converter.today_nepali_calendar

        week_day_name_in_english = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliDatePickerLang.ENGLISH
        )
        full_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliDatePickerLang.NEPALI
        )
        medium_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.MEDIUM, language=NepaliDatePickerLang.NEPALI
        )

        month_name_in_english = NepaliDateConverter.get_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliDatePickerLang.ENGLISH
        )
        month_name_in_nepali = NepaliDateConverter.get_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliDatePickerLang.NEPALI
        )
        short_month_name_in_nepali = NepaliDateConverter.get_month_name(
            month=custom_calendar.month, format=NameFormat.SHORT, language=NepaliDatePickerLang.NEPALI
        )

        day_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month))
        month_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.month))
        year_in_nepali = NepaliDateConverter.localize_number(str(custom_calendar.year), NepaliDatePickerLang.NEPALI)

        english_locale = NepaliDateLocale()

        correct_formatted_date_in_english = f"{month_name_in_english} {custom_calendar.day_of_month}, {custom_calendar.year}"
        to_test_formatted_date_in_english = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, english_locale)

        self.assertEqual(correct_formatted_date_in_english, to_test_formatted_date_in_english)

        full_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL
        )
        correct_full_nepali_formatted_date = f"{full_week_day_name_in_nepali}, {month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_full_nepali_formatted_date = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, full_nepali_locale)

        self.assertEqual(correct_full_nepali_formatted_date, to_test_full_nepali_formatted_date)

        mix_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.MEDIUM,
            month_name=NameFormat.SHORT
        )
        correct_mix_nepali_formatted_date = f"{medium_week_day_name_in_nepali}, {short_month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_mix_nepali_formatted_date = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, mix_nepali_locale)

        self.assertEqual(correct_mix_nepali_formatted_date, to_test_mix_nepali_formatted_date)

        day_in_nepali_with_leading_zero = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month).zfill(2))
        month_in_nepali_with_leading_zero = NepaliDateConverter.localize_number(str(custom_calendar.month).zfill(2), NepaliDatePickerLang.NEPALI)

        compat_year = year_in_nepali[2:4]  # Alternatively, year_in_nepali[-2:]
        compat_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.COMPACT_YMD
        )
        correct_compat_nepali_formatted_date = f"{compat_year}/{month_in_nepali_with_leading_zero}/{day_in_nepali_with_leading_zero}"
        to_test_compat_nepali_formatted_date = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, compat_nepali_locale)

        self.assertEqual(correct_compat_nepali_formatted_date, to_test_compat_nepali_formatted_date)


    def test_format_english_date_random_date_get_formatted_date_in_string_by_locale(self):
        english_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.ENGLISH,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.FULL,
            month_name=NameFormat.FULL
        )

        nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.MEDIUM,
            month_name=NameFormat.FULL
        )

        full_format_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.FULL,
            month_name=NameFormat.FULL
        )

        to_test_formatted_date_in_english = NepaliDateConverter.format_english_date(
            year=2024, month=3, day_of_month=15, day_of_week=3, locale=english_locale
        )
        formatted_date_in_english = "Tuesday, March 15, 2024"

        to_test_formatted_date_in_nepali = NepaliDateConverter.format_english_date(
            year=2024, month=6, day_of_month=2, day_of_week=5, locale=nepali_locale
        )
        formatted_date_in_nepali = "२०२४ जुन २"

        to_test_full_formatted_date_in_nepali = NepaliDateConverter.format_english_date(
            year=2024, month=2, day_of_month=2, day_of_week=5, locale=full_format_nepali_locale
        )
        full_formatted_date_in_nepali = "बिहिबार, फेब्रुअरी २, २०२४"

        self.assertEqual(formatted_date_in_english, to_test_formatted_date_in_english)
        self.assertEqual(formatted_date_in_nepali, to_test_formatted_date_in_nepali)
        self.assertEqual(full_formatted_date_in_nepali, to_test_full_formatted_date_in_nepali)

    def test_format_english_date_using_other_helper_function_of_names_custom_calendar_date_get_formatted_date_in_string(self):
        date_converter = NepaliDateConverter()
        custom_calendar = date_converter.today_nepali_calendar
        today_nepali_date = date_converter.today_nepali_calendar
        custom_calendar = NepaliDateConverter.convert_nepali_to_english(
            today_nepali_date.year, today_nepali_date.month, today_nepali_date.day_of_month
        )

        week_day_name_in_english = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliDatePickerLang.ENGLISH
        )
        full_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliDatePickerLang.NEPALI
        )
        medium_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.MEDIUM, language=NepaliDatePickerLang.NEPALI
        )

        month_name_in_english = NepaliDateConverter.get_english_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliDatePickerLang.ENGLISH
        )
        month_name_in_nepali = NepaliDateConverter.get_english_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliDatePickerLang.NEPALI
        )
        short_month_name_in_nepali = NepaliDateConverter.get_english_month_name(
            month=custom_calendar.month, format=NameFormat.SHORT, language=NepaliDatePickerLang.NEPALI
        )

        day_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month))
        month_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.month))
        year_in_nepali = NepaliDateConverter.localize_number(str(custom_calendar.year), NepaliDatePickerLang.NEPALI)

        english_locale = NepaliDateLocale()

        correct_formatted_date_in_english = f"{month_name_in_english} {custom_calendar.day_of_month}, {custom_calendar.year}"
        to_test_formatted_date_in_english = NepaliDateConverter.format_english_date_from_calendar(custom_calendar, english_locale)

        self.assertEqual(correct_formatted_date_in_english, to_test_formatted_date_in_english)

        full_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL
        )
        correct_full_nepali_formatted_date = f"{full_week_day_name_in_nepali}, {month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_full_nepali_formatted_date = NepaliDateConverter.format_english_date_from_calendar(custom_calendar, full_nepali_locale)

        self.assertEqual(correct_full_nepali_formatted_date, to_test_full_nepali_formatted_date)

        mix_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.MEDIUM,
            month_name=NameFormat.SHORT
        )
        correct_mix_nepali_formatted_date = f"{medium_week_day_name_in_nepali}, {short_month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_mix_nepali_formatted_date = NepaliDateConverter.format_english_date_from_calendar(custom_calendar, mix_nepali_locale)

        self.assertEqual(correct_mix_nepali_formatted_date, to_test_mix_nepali_formatted_date)

        day_in_nepali_with_leading_zero = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month).zfill(2))
        month_in_nepali_with_leading_zero = NepaliDateConverter.localize_number(str(custom_calendar.month).zfill(2), NepaliDatePickerLang.NEPALI)

        compat_year = year_in_nepali[2:4]
        compat_nepali_locale = NepaliDateLocale(
            language=NepaliDatePickerLang.NEPALI,
            date_format=NepaliDateFormatStyle.COMPACT_YMD
        )
        correct_compat_nepali_formatted_date = f"{compat_year}/{month_in_nepali_with_leading_zero}/{day_in_nepali_with_leading_zero}"
        to_test_compat_nepali_formatted_date = NepaliDateConverter.format_english_date_from_calendar(custom_calendar, compat_nepali_locale)

        self.assertEqual(correct_compat_nepali_formatted_date, to_test_compat_nepali_formatted_date)
        
    def test_format_time_in_english_random_simple_time(self):
        time = SimpleTime(16, 30, 48, 22)

        time_12_hour = NepaliDateConverter.get_formatted_time_in_english(time)
        correct_12_hour_formatted_time = "4:30 PM"
        self.assertEqual(correct_12_hour_formatted_time, time_12_hour)

        time_24_hour = NepaliDateConverter.get_formatted_time_in_english(time, False)
        correct_24_hour_formatted_time = "16:30"
        self.assertEqual(correct_24_hour_formatted_time, time_24_hour)

    def test_format_time_in_nepali_random_simple_time(self):
        time = SimpleTime(16, 30, 48, 22)

        time_12_hour = NepaliDateConverter.get_formatted_time_in_nepali(time)
        correct_12_hour_formatted_time = "दिउँसो ४ : ३०"
        self.assertEqual(correct_12_hour_formatted_time, time_12_hour)

        time_24_hour = NepaliDateConverter.get_formatted_time_in_nepali(time, False)
        correct_24_hour_formatted_time = "१६ : ३०"
        self.assertEqual(correct_24_hour_formatted_time, time_24_hour)

    def test_format_time_to_iso_format_random_dates(self):
            nepali_date = SimpleDate(2081, 5, 24)
            time = SimpleTime(14, 45, 15, 0)

            nepali_date_iso_format = NepaliDateConverter.format_nepali_datetime_to_iso(nepali_date, time)
            correct_nepali_date_iso_format = "2024-09-09T09:00:15Z"
            self.assertEqual(correct_nepali_date_iso_format, nepali_date_iso_format)

            english_date = SimpleDate(2024, 9, 9)
            english_date_iso_format = NepaliDateConverter.format_english_date_nepali_time_to_iso(english_date, time)
            correct_english_date_iso_format = "2024-09-09T09:00:15Z"
            self.assertEqual(correct_english_date_iso_format, english_date_iso_format)

            self.assertEqual(nepali_date_iso_format, english_date_iso_format)

    def test_format_and_compare_time_to_iso_format_today_english_and_nepali_date(self):
        date_convert = NepaliDateConverter()
        time = SimpleTime(14, 30, 15, 0)

        nepali_date = date_convert.today_nepali_calendar.to_simple_date()
        nepali_date_iso_format = NepaliDateConverter.format_nepali_datetime_to_iso(nepali_date, time)

        english_date = date_convert.today_english_simple_date
        english_date_iso_format = NepaliDateConverter.format_english_date_nepali_time_to_iso(english_date, time)

        self.assertEqual(nepali_date_iso_format, english_date_iso_format)
        
    def test_replace_delimiters_of_string_random_date_string_with_delimiter(self):
        original_date = "2024/06/21"
        new_delimiter = "-"
        formatted_date = NepaliDateConverter.replace_delimiter(original_date, new_delimiter)
        correct_formatted_date = "2024-06-21"
        self.assertEqual(correct_formatted_date, formatted_date)

        original_nepali_date = "२०२४/०६/२१"
        formatted_nepali_date = NepaliDateConverter.replace_delimiter(original_nepali_date, new_delimiter)
        correct_formatted_nepali_date = "२०२४-०६-२१"
        self.assertEqual(correct_formatted_nepali_date, formatted_nepali_date)

        original_time = "09:45 AM"
        new_delimiter_space = " "
        old_delimiter = ":"
        formatted_time_with_space = NepaliDateConverter.replace_delimiter(original_time, new_delimiter_space, old_delimiter)
        corrected_formatted_time_with_space = "09 45 AM"
        self.assertEqual(corrected_formatted_time_with_space, formatted_time_with_space)


if __name__ == "__main__":
    unittest.main()