import unittest
from datetime import date
from unittest.mock import Mock
from graphs import date_ranges


class DateRangesTests(unittest.TestCase):
    def setUp(self):
        self.setup_mocks()
        self.setup_mock_return_values()

    def setup_mocks(self):
        self.date_mock = Mock()
        self.today_mock = Mock()
        pass

    def setup_mock_return_values(self):
        self.date_mock.today.return_value = self.today_mock
        self.date_mock.return_value = "2016-01-01"
        self.today_mock.isocalendar.return_value = (2016, 0, 1)

    def test_get_week_start_date(self):
        # Arrange
        expected_result = date(2015, 12, 28)

        # Execute
        result = date_ranges.get_week_start_date(2016, 0)

        # Checks
        self.assertEqual(expected_result, result)

    def test_get_date_ranges_for_this_year(self):
        # Arrange
        date_ranges.date = self.date_mock
        get_week_start_date_mock = Mock()
        get_week_start_date_mock.return_value = date(2015, 12, 28)

        date_ranges.get_week_start_date = get_week_start_date_mock

        # Execute
        result = date_ranges.get_date_ranges_for_this_year()

        # Checks
        self.assertEqual({'week0': {'end_date': '20160103', 'start_date': '20151228'}}, result)
