import unittest

from nepali_calendar_utils.data.custom_calendar import SimpleDate
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.nepali_selectable_dates import NepaliSelectableDates


def cal(year, month, day):
    return NepaliDateConverter.get_nepali_calendar(year, month, day)


class TestSelectableDates(unittest.TestCase):
    def test_base_allows_everything(self):
        base = NepaliSelectableDates()
        self.assertTrue(base.is_selectable_date(cal(2081, 5, 24)))
        self.assertTrue(base.is_selectable_year(2081))

    def test_before_date_selectable_excludes_boundary_by_default(self):
        sel = NepaliDateConverter.before_date_selectable(SimpleDate(2081, 5, 24))
        self.assertTrue(sel.is_selectable_date(cal(2081, 5, 23)))
        self.assertFalse(sel.is_selectable_date(cal(2081, 5, 24)))
        self.assertFalse(sel.is_selectable_date(cal(2081, 5, 25)))

    def test_before_date_selectable_includes_boundary_when_asked(self):
        sel = NepaliDateConverter.before_date_selectable(SimpleDate(2081, 5, 24), include_date=True)
        self.assertTrue(sel.is_selectable_date(cal(2081, 5, 24)))

    def test_before_date_selectable_year(self):
        sel = NepaliDateConverter.before_date_selectable(SimpleDate(2081, 5, 24))
        self.assertTrue(sel.is_selectable_year(2080))
        self.assertTrue(sel.is_selectable_year(2081))
        self.assertFalse(sel.is_selectable_year(2082))

    def test_after_date_selectable(self):
        sel = NepaliDateConverter.after_date_selectable(SimpleDate(2081, 5, 24))
        self.assertTrue(sel.is_selectable_date(cal(2081, 5, 25)))
        self.assertFalse(sel.is_selectable_date(cal(2081, 5, 24)))
        self.assertFalse(sel.is_selectable_date(cal(2081, 5, 23)))
        self.assertTrue(sel.is_selectable_year(2082))
        self.assertFalse(sel.is_selectable_year(2080))

    def test_after_date_selectable_include(self):
        sel = NepaliDateConverter.after_date_selectable(SimpleDate(2081, 5, 24), include_date=True)
        self.assertTrue(sel.is_selectable_date(cal(2081, 5, 24)))

    def test_date_range_selectable_default_exclusive(self):
        sel = NepaliDateConverter.date_range_selectable(SimpleDate(2081, 5, 10), SimpleDate(2081, 5, 20))
        self.assertFalse(sel.is_selectable_date(cal(2081, 5, 10)))
        self.assertTrue(sel.is_selectable_date(cal(2081, 5, 15)))
        self.assertFalse(sel.is_selectable_date(cal(2081, 5, 20)))

    def test_date_range_selectable_inclusive(self):
        sel = NepaliDateConverter.date_range_selectable(
            SimpleDate(2081, 5, 10), SimpleDate(2081, 5, 20),
            include_min_date=True, include_max_date=True,
        )
        self.assertTrue(sel.is_selectable_date(cal(2081, 5, 10)))
        self.assertTrue(sel.is_selectable_date(cal(2081, 5, 20)))
        self.assertFalse(sel.is_selectable_date(cal(2081, 5, 21)))

    def test_date_range_selectable_year(self):
        sel = NepaliDateConverter.date_range_selectable(SimpleDate(2080, 1, 1), SimpleDate(2082, 12, 30))
        self.assertTrue(sel.is_selectable_year(2081))
        self.assertFalse(sel.is_selectable_year(2079))
        self.assertFalse(sel.is_selectable_year(2083))


if __name__ == "__main__":
    unittest.main()
