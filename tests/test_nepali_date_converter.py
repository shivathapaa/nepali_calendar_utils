import unittest
from nepali_calendar_utils.data.custom_calendar import *
from nepali_calendar_utils.calendar_model.nepali_calendar_model import NepaliCalendarModel
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.nepali_date_locale import NameFormat, NepaliDateFormatStyle, NepaliDateLocale, NepaliCalendarUtilsLang

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
            language=NepaliCalendarUtilsLang.ENGLISH,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.FULL,
            month_name=NameFormat.FULL
        )

        nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.MEDIUM,
            month_name=NameFormat.FULL
        )

        full_format_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
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
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.ENGLISH
        )
        full_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.NEPALI
        )
        medium_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.MEDIUM, language=NepaliCalendarUtilsLang.NEPALI
        )

        month_name_in_english = NepaliDateConverter.get_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.ENGLISH
        )
        month_name_in_nepali = NepaliDateConverter.get_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.NEPALI
        )
        short_month_name_in_nepali = NepaliDateConverter.get_month_name(
            month=custom_calendar.month, format=NameFormat.SHORT, language=NepaliCalendarUtilsLang.NEPALI
        )

        day_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month))
        month_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.month))
        year_in_nepali = NepaliDateConverter.localize_number(str(custom_calendar.year), NepaliCalendarUtilsLang.NEPALI)

        english_locale = NepaliDateLocale()

        correct_formatted_date_in_english = f"{month_name_in_english} {custom_calendar.day_of_month}, {custom_calendar.year}"
        to_test_formatted_date_in_english = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, english_locale)

        self.assertEqual(correct_formatted_date_in_english, to_test_formatted_date_in_english)

        full_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL
        )
        correct_full_nepali_formatted_date = f"{full_week_day_name_in_nepali}, {month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_full_nepali_formatted_date = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, full_nepali_locale)

        self.assertEqual(correct_full_nepali_formatted_date, to_test_full_nepali_formatted_date)

        mix_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.MEDIUM,
            month_name=NameFormat.SHORT
        )
        correct_mix_nepali_formatted_date = f"{medium_week_day_name_in_nepali}, {short_month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_mix_nepali_formatted_date = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, mix_nepali_locale)

        self.assertEqual(correct_mix_nepali_formatted_date, to_test_mix_nepali_formatted_date)

        day_in_nepali_with_leading_zero = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month).zfill(2))
        month_in_nepali_with_leading_zero = NepaliDateConverter.localize_number(str(custom_calendar.month).zfill(2), NepaliCalendarUtilsLang.NEPALI)

        compat_year = year_in_nepali[2:4]  # Alternatively, year_in_nepali[-2:]
        compat_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.COMPACT_YMD
        )
        correct_compat_nepali_formatted_date = f"{compat_year}/{month_in_nepali_with_leading_zero}/{day_in_nepali_with_leading_zero}"
        to_test_compat_nepali_formatted_date = NepaliDateConverter.format_nepali_date_from_calendar(custom_calendar, compat_nepali_locale)

        self.assertEqual(correct_compat_nepali_formatted_date, to_test_compat_nepali_formatted_date)


    def test_format_english_date_random_date_get_formatted_date_in_string_by_locale(self):
        english_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.ENGLISH,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.FULL,
            month_name=NameFormat.FULL
        )

        nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.MEDIUM,
            month_name=NameFormat.FULL
        )

        full_format_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
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
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.ENGLISH
        )
        full_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.NEPALI
        )
        medium_week_day_name_in_nepali = NepaliDateConverter.get_weekday_name(
            day_of_week=custom_calendar.day_of_week, format=NameFormat.MEDIUM, language=NepaliCalendarUtilsLang.NEPALI
        )

        month_name_in_english = NepaliDateConverter.get_english_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.ENGLISH
        )
        month_name_in_nepali = NepaliDateConverter.get_english_month_name(
            month=custom_calendar.month, format=NameFormat.FULL, language=NepaliCalendarUtilsLang.NEPALI
        )
        short_month_name_in_nepali = NepaliDateConverter.get_english_month_name(
            month=custom_calendar.month, format=NameFormat.SHORT, language=NepaliCalendarUtilsLang.NEPALI
        )

        day_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month))
        month_in_nepali = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.month))
        year_in_nepali = NepaliDateConverter.localize_number(str(custom_calendar.year), NepaliCalendarUtilsLang.NEPALI)

        english_locale = NepaliDateLocale()

        correct_formatted_date_in_english = f"{month_name_in_english} {custom_calendar.day_of_month}, {custom_calendar.year}"
        to_test_formatted_date_in_english = NepaliDateConverter.format_english_date_from_calendar(custom_calendar, english_locale)

        self.assertEqual(correct_formatted_date_in_english, to_test_formatted_date_in_english)

        full_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL
        )
        correct_full_nepali_formatted_date = f"{full_week_day_name_in_nepali}, {month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_full_nepali_formatted_date = NepaliDateConverter.format_english_date_from_calendar(custom_calendar, full_nepali_locale)

        self.assertEqual(correct_full_nepali_formatted_date, to_test_full_nepali_formatted_date)

        mix_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
            date_format=NepaliDateFormatStyle.FULL,
            week_day_name=NameFormat.MEDIUM,
            month_name=NameFormat.SHORT
        )
        correct_mix_nepali_formatted_date = f"{medium_week_day_name_in_nepali}, {short_month_name_in_nepali} {day_in_nepali}, {year_in_nepali}"
        to_test_mix_nepali_formatted_date = NepaliDateConverter.format_english_date_from_calendar(custom_calendar, mix_nepali_locale)

        self.assertEqual(correct_mix_nepali_formatted_date, to_test_mix_nepali_formatted_date)

        day_in_nepali_with_leading_zero = NepaliDateConverter.convert_to_nepali_number(str(custom_calendar.day_of_month).zfill(2))
        month_in_nepali_with_leading_zero = NepaliDateConverter.localize_number(str(custom_calendar.month).zfill(2), NepaliCalendarUtilsLang.NEPALI)

        compat_year = year_in_nepali[2:4]
        compat_nepali_locale = NepaliDateLocale(
            language=NepaliCalendarUtilsLang.NEPALI,
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
            time = SimpleTime(14, 45, 15, 123456789)

            nepali_date_iso_format = NepaliDateConverter.format_nepali_datetime_to_iso(nepali_date, time)
            correct_nepali_date_iso_format = "2024-09-09T09:00:15.123456Z"
            self.assertEqual(correct_nepali_date_iso_format, nepali_date_iso_format)

            english_date = SimpleDate(2024, 9, 9)
            english_date_iso_format = NepaliDateConverter.format_english_date_nepali_time_to_iso(english_date, time)
            correct_english_date_iso_format = "2024-09-09T09:00:15.123456Z"
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
        
    def test_convert_iso_to_nepali_calendar_and_time(self):
        iso_string = "2024-09-09T09:00:15Z"
        custom_datetime = NepaliDateConverter.get_nepali_date_time_from_iso_format(iso_string)
        expected_calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        expected_time = SimpleTime(14, 45, 15, 0)

        self.assertEqual(expected_calendar, custom_datetime.custom_calendar)
        self.assertEqual(expected_time, custom_datetime.simple_time)

        iso_string2 = "2020-08-30T18:43:00.123456Z"
        custom_datetime2 = NepaliDateConverter.get_nepali_date_time_from_iso_format(iso_string2)
        expected_calendar2 = NepaliDateConverter.get_nepali_calendar(2077, 5, 15)
        expected_time2 = SimpleTime(0, 28, 0, 123456000)

        self.assertEqual(expected_calendar2, custom_datetime2.custom_calendar)
        self.assertEqual(expected_time2, custom_datetime2.simple_time)
        
    def test_various_iso_patterns_to_nepali_calendar_and_time(self):
        test_cases = [
            ("2020-08-30T18:43:00Z", (2077, 5, 15), SimpleTime(0, 28, 0, 0)),
            ("2020-08-30T18:43:00.502Z", (2077, 5, 15), SimpleTime(0, 28, 0, 502000000)),
            ("2020-08-30T18:43:00.123456Z", (2077, 5, 15), SimpleTime(0, 28, 0, 123456000)),
            ("2020-08-30T18:40:00+00:00", (2077, 5, 15), SimpleTime(0, 25, 0, 0)),
            ("2020-08-30T18:40:00+00:00:00", (2077, 5, 15), SimpleTime(0, 25, 0, 0)),
            ("2011-11-04", (2068, 7, 18), SimpleTime(0, 0, 0, 0)),
            ("2011-11-04 00:05:23.283", (2068, 7, 18), SimpleTime(0, 5, 23, 283000000)),
            ("2011-11-04 00:05:23.283+00:00", (2068, 7, 18), SimpleTime(5, 50, 23, nanosecond=283000000)),
            ("2011-11-04T00:05:23+04:00", (2068, 7, 18), SimpleTime(1, 50, 23, 0)),
        ]

        for iso_string, (ny, nm, nd), expected_time in test_cases:
            with self.subTest(iso_string=iso_string):
                result = NepaliDateConverter.get_nepali_date_time_from_iso_format(iso_string)
                expected_calendar = NepaliDateConverter.get_nepali_calendar(ny, nm, nd)
                self.assertEqual(result.custom_calendar, expected_calendar)
                self.assertEqual(result.simple_time, expected_time)


    def test_convert_iso_to_english_calendar_and_nepali_time(self):
        iso_string = "2024-09-09T09:00:15Z"
        custom_datetime = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(iso_string)

        expected_nepali_calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        expected_english_calendar = NepaliDateConverter.convert_nepali_to_english(
            expected_nepali_calendar.year,
            expected_nepali_calendar.month,
            expected_nepali_calendar.day_of_month
        )
        expected_time = SimpleTime(14, 45, 15, 0)

        self.assertEqual(expected_english_calendar, custom_datetime.custom_calendar)
        self.assertEqual(expected_time, custom_datetime.simple_time)

        iso_string2 = "2020-01-01T23:59:59.123456Z"
        custom_datetime2 = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(iso_string2)

        expected_nepali_calendar2 = NepaliDateConverter.get_nepali_calendar(2076, 9, 17)
        expected_english_calendar2 = NepaliDateConverter.convert_nepali_to_english(
            expected_nepali_calendar2.year,
            expected_nepali_calendar2.month,
            expected_nepali_calendar2.day_of_month
        )
        expected_time2 = SimpleTime(5, 44, 59, 123456000)

        self.assertEqual(expected_english_calendar2, custom_datetime2.custom_calendar)
        self.assertEqual(expected_time2, custom_datetime2.simple_time)
        
    def test_various_iso_patterns_to_english_calendar_and_nepali_time(self):
        test_cases = [
            ("2020-08-30T18:43:00Z", (2077, 5, 15), SimpleTime(0, 28, 0, 0)),
            ("2020-08-30T18:43:00.502Z", (2077, 5, 15), SimpleTime(0, 28, 0, 502000000)),
            ("2020-08-30T18:43:00.123456Z", (2077, 5, 15), SimpleTime(0, 28, 0, 123456000)),
            ("2020-08-30T18:40:00+00:00", (2077, 5, 15), SimpleTime(0, 25, 0, 0)),
            ("2020-08-30T18:40:00+00:00:00", (2077, 5, 15), SimpleTime(0, 25, 0, 0)),
            ("2011-11-04", (2068, 7, 18), SimpleTime(0, 0, 0, 0)),
            ("2011-11-04 00:05:23.283", (2068, 7, 18), SimpleTime(0, 5, 23, 283000000)),
            ("2011-11-04 00:05:23.283+00:00", (2068, 7, 18), SimpleTime(5, 50, 23, 283000000)),
            ("2011-11-04T00:05:23+04:00", (2068, 7, 18), SimpleTime(1, 50, 23, 0)),
        ]

        for iso_string, (ny, nm, nd), expected_time in test_cases:
            with self.subTest(iso_string=iso_string):
                custom_datetime = NepaliDateConverter.get_english_date_nepali_time_from_iso_format(iso_string)
                nepali_calendar = NepaliDateConverter.get_nepali_calendar(ny, nm, nd)
                expected_english_calendar = NepaliDateConverter.convert_nepali_to_english(
                    nepali_calendar.year, nepali_calendar.month, nepali_calendar.day_of_month
                )
                self.assertEqual(custom_datetime.custom_calendar, expected_english_calendar)
                self.assertEqual(custom_datetime.simple_time, expected_time)

        
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

    
    def test_format_nepali_datetime_full_pattern_returns_correct_format(self):
        test_calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        test_time = SimpleTime(14, 45, 15, 123000000)

        def check(pattern, expected, lang=NepaliCalendarUtilsLang.NEPALI):
            result = NepaliDateConverter.format_nepali_date_time_by_unicode_pattern(pattern, test_calendar, test_time, lang)
            self.assertEqual(expected, result, f"Pattern: {pattern}")

        check("yyyy", "२०८१")
        check("yy", "८१")
        check("MMMM", "भदौ")
        check("MMM", "भ")
        check("MM", "०५")
        check("M", "५")
        check("dd", "२४")
        check("d", "२४")
        check("D", "१५०")
        check("w", "२३")

        check("EEEE", "Monday", lang=NepaliCalendarUtilsLang.ENGLISH)
        check("EEEE", "सोमबार")
        check("E", "सोम")
        check("EEEEE", "सो")

        check("ee", "०२")
        check("e", "२")

        check("HH", "१४")
        check("H", "१४")
        check("hh", "०२")
        check("h", "२")
        check("mm", "४५")
        check("m", "४५")
        check("ss", "१५")
        check("s", "१५")

        check("SSSS", "१२३०")
        check("SSS", "१२३")
        check("SS", "१२")
        check("S", "१")

        check("a", "दिउँसो")
        check("A", "दिउँसो")

        check("yyyy-MM-dd E a hh:mm:ss", "२०८१-०५-२४ सोम दिउँसो ०२:४५:१५")

    def test_format_english_datetime_full_pattern_returns_correct_format(self):
        test_calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        test_time = SimpleTime(14, 45, 15, 123000000)

        def check(pattern, expected):
            result = NepaliDateConverter.format_english_date_time_by_unicode_pattern(pattern, test_calendar, test_time)
            self.assertEqual(expected, result, f"Pattern: {pattern}")

        check("yyyy", "2081")
        check("yy", "81")
        check("MMMM", "May")
        check("MMM", "May")
        check("MM", "05")
        check("M", "5")
        check("dd", "24")
        check("d", "24")
        check("D", "150")
        check("w", "23")

        check("EEEE", "Monday")
        check("E", "Mon")
        check("EEEEE", "M")

        check("ee", "02")
        check("e", "2")

        check("HH", "14")
        check("H", "14")
        check("hh", "02")
        check("h", "2")
        check("mm", "45")
        check("m", "45")
        check("ss", "15")
        check("s", "15")

        check("SSSS", "1230")
        check("SSS", "123")
        check("SS", "12")
        check("S", "1")

        check("a", "pm")
        check("A", "PM")

        check("yyyy-MM-dd E A hh:mm:ss", "2081-05-24 Mon PM 02:45:15")

    def test_format_datetime_midnight_and_end_of_day_correct_format(self):
        calendar = NepaliDateConverter.get_nepali_calendar(2081, 1, 1)

        midnight = SimpleTime(0, 0, 0, 0)
        end_of_day = SimpleTime(23, 59, 59, 999000000)

        def check(time, expected):
            result = NepaliDateConverter.format_english_date_time_by_unicode_pattern("HH:mm:ss.SSS a", calendar, time)
            self.assertEqual(expected, result)

        check(midnight, "00:00:00.000 am")
        check(end_of_day, "23:59:59.999 pm")

    def test_format_datetime_empty_pattern_returns_empty_string(self):
        calendar = NepaliDateConverter.get_nepali_calendar(2081, 1, 1)
        result = NepaliDateConverter.format_english_date_time_by_unicode_pattern("", calendar)
        self.assertEqual("", result)

    def test_format_datetime_unsupported_tokens_ignores_them(self):
        calendar = NepaliDateConverter.get_nepali_calendar(2081, 1, 1)
        pattern = "yyyy-MM-XX HH:mm:ss ??"
        result = NepaliDateConverter.format_english_date_time_by_unicode_pattern(pattern, calendar, SimpleTime(10, 30, 0, 0))
        self.assertEqual("2081-01-XX 10:30:00 ??", result)

    def test_format_datetime_all_tokens_mixed_returns_complete_format(self):
        calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        time = SimpleTime(14, 45, 15, 123000000)
        pattern = "yyyy yy MMMM MMM MM M dd d D EEEE E EEEEE ee e w HH H hh h mm m ss s SSSS SSS SS S a A"
        expected = "2081 81 May May 05 5 24 24 150 Monday Mon M 02 2 23 14 14 02 2 45 45 15 15 1230 123 12 1 pm PM"

        result = NepaliDateConverter.format_english_date_time_by_unicode_pattern(pattern, calendar, time)
        self.assertEqual(expected, result)

    def test_format_nepali_datetime_all_tokens_mixed_returns_complete_format(self):
        calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        time = SimpleTime(14, 45, 15, 123000000)
        pattern = "yyyy yy MMMM MMM MM M dd d D EEEE E EEEEE ee e w HH H hh h mm m ss s SSSS SSS SS S a A"
        expected = "२०८१ ८१ भदौ भ ०५ ५ २४ २४ १५० सोमबार सोम सो ०२ २ २३ १४ १४ ०२ २ ४५ ४५ १५ १५ १२३० १२३ १२ १ दिउँसो दिउँसो"

        result = NepaliDateConverter.format_nepali_date_time_by_unicode_pattern(pattern, calendar, time)
        self.assertEqual(expected, result)

    def test_format_only_date_english_and_nepali(self):
        calendar = NepaliDateConverter.get_nepali_calendar(2081, 5, 24)
        en = NepaliDateConverter.format_english_date_time_by_unicode_pattern("yyyy-MM-dd", calendar)
        np = NepaliDateConverter.format_nepali_date_time_by_unicode_pattern("yyyy-MM-dd", calendar, language=NepaliCalendarUtilsLang.NEPALI)

        self.assertEqual("2081-05-24", en)
        self.assertEqual("२०८१-०५-२४", np)

    def test_format_only_time_am_pm_language_sensitive(self):
        morning = SimpleTime(9, 5, 3, 45000000)
        night = SimpleTime(22, 30, 0, 0)

        self.assertEqual("09:05:03 am", NepaliDateConverter.format_time_by_unicode_pattern("hh:mm:ss a", morning, NepaliCalendarUtilsLang.ENGLISH))
        self.assertEqual("१०:३०:०० राति", NepaliDateConverter.format_time_by_unicode_pattern("hh:mm:ss a", night, NepaliCalendarUtilsLang.NEPALI))

    def test_format_ampm_language_difference(self):
        morning = SimpleTime(5, 0, 0, 0)
        evening = SimpleTime(18, 0, 0, 0)

        self.assertEqual("am", NepaliDateConverter.format_time_by_unicode_pattern("a", morning, NepaliCalendarUtilsLang.ENGLISH))
        self.assertEqual("pm", NepaliDateConverter.format_time_by_unicode_pattern("a", evening, NepaliCalendarUtilsLang.ENGLISH))

        self.assertEqual("बिहान", NepaliDateConverter.format_time_by_unicode_pattern("a", morning, NepaliCalendarUtilsLang.NEPALI))
        self.assertEqual("साँझ", NepaliDateConverter.format_time_by_unicode_pattern("a", evening, NepaliCalendarUtilsLang.NEPALI))

        self.assertEqual("AM", NepaliDateConverter.format_time_by_unicode_pattern("A", morning, NepaliCalendarUtilsLang.ENGLISH))
        self.assertEqual("PM", NepaliDateConverter.format_time_by_unicode_pattern("A", evening, NepaliCalendarUtilsLang.ENGLISH))

        self.assertEqual("बिहान", NepaliDateConverter.format_time_by_unicode_pattern("A", morning, NepaliCalendarUtilsLang.NEPALI))
        self.assertEqual("साँझ", NepaliDateConverter.format_time_by_unicode_pattern("A", evening, NepaliCalendarUtilsLang.NEPALI))

if __name__ == "__main__":
    unittest.main()