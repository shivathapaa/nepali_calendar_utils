"""The era a calendar system carries, and reading a calendar back as one."""

import unittest

from nepali_calendar_utils.data.calendar_system import CalendarSystem
from nepali_calendar_utils.data.custom_calendar import CustomCalendar


def _calendar(era: int) -> CustomCalendar:
    return CustomCalendar(
        year=2082,
        month=1,
        day_of_month=1,
        era=era,
        first_day_of_month=1,
        last_day_of_month=3,
        total_days_in_month=31,
    )


class TestCalendarSystem(unittest.TestCase):

    def test_era_numbers_match_the_calendars(self):
        self.assertEqual(2, CalendarSystem.BIKRAM_SAMBAT.era)
        self.assertEqual(1, CalendarSystem.GREGORIAN.era)

    def test_opposite_toggles(self):
        self.assertIs(CalendarSystem.GREGORIAN, CalendarSystem.BIKRAM_SAMBAT.opposite())
        self.assertIs(CalendarSystem.BIKRAM_SAMBAT, CalendarSystem.GREGORIAN.opposite())

    def test_opposite_twice_is_identity(self):
        for system in CalendarSystem:
            self.assertIs(system, system.opposite().opposite())

    def test_from_era_reads_both(self):
        self.assertIs(CalendarSystem.BIKRAM_SAMBAT, CalendarSystem.from_era(2))
        self.assertIs(CalendarSystem.GREGORIAN, CalendarSystem.from_era(1))

    def test_from_era_returns_none_for_anything_else(self):
        for era in (-1, 0, 3, 99):
            self.assertIsNone(CalendarSystem.from_era(era))


class TestCustomCalendarSystem(unittest.TestCase):

    def test_reads_the_system_from_the_era(self):
        self.assertIs(CalendarSystem.BIKRAM_SAMBAT, _calendar(2).calendar_system)
        self.assertIs(CalendarSystem.GREGORIAN, _calendar(1).calendar_system)

    def test_unrecognised_era_falls_back_to_bikram_sambat(self):
        # A restored or parsed value should not crash a caller that only wants to draw a grid.
        self.assertIs(CalendarSystem.BIKRAM_SAMBAT, _calendar(0).calendar_system)
        self.assertIs(CalendarSystem.BIKRAM_SAMBAT, _calendar(7).calendar_system)


if __name__ == "__main__":
    unittest.main()
