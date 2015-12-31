import data_collector
import time
import unittest
import unittest.mock
from unittest.mock import patch
from utilities.database_handler import DatabaseHandler


class DataCollectorTests(unittest.TestCase):
    def setUp(self):
        self.valid_json_data_mock = {'text': 'THIS IS A SAMPLE TWEET', 'user': {'id_str': '0000', 'lang': 'pt', 'location': 'Sorocaba-SP'} }
        self.valid_location_mock = 'Ireland'
        self.invalid_location_mock = None
        self.valid_text_mock = "this is valid text because it conatins the word flu and no banned words"
        self.invalid_text_mock = "this is invalid because it contains the word rt for retweet"
        self.valid_language_mock = 'en'
        self.invalid_language_mock = 'rt'
        self.test_listener = data_collector.Listener()
        self.mock_record = {}
        self.mock_latitude = 0000
        self.mock_longitude = 0000
        self.mock_timestamp = 00000000


    def test_get_data_from_json_returns_userId_text_language_location(self):
        # Get time tweet picked up
        mock_timestamp = time.strftime("%d%m%Y")

        user_id, text, language, location, timestamp = self.test_listener.get_data_from_json_data(self.valid_json_data_mock)

        self.assertEquals(user_id, '0000')
        self.assertEquals(text, 'this is a sample tweet')
        self.assertEquals(language, 'pt')
        self.assertEquals(location,'Sorocaba-SP')
        self.assertEquals(timestamp, mock_timestamp)

    def test_get_data_from_json_returns_unknown_invalidtext_unknown_None_when_keyerror_raised(self):
        # Get time tweet picked up
        mock_timestamp = time.strftime("%d%m%Y")

        mock_invalid_json_data_mock = { }

        user_id, text, language, location, timestamp = self.test_listener.get_data_from_json_data(mock_invalid_json_data_mock)

        self.assertEquals(user_id, 'unknown')
        self.assertEquals(text, 'invalid text')
        self.assertEquals(language, 'unknown')
        self.assertEquals(location,None)
        self.assertEquals(timestamp, mock_timestamp)

    def test_add_location_to_record(self):

        self.test_listener.add_location_attributes_to_record('test address', self.mock_latitude, self.mock_longitude, self.mock_record)

        self.assertEqual(self.mock_record['address'], 'test address')
        self.assertEqual(self.mock_record['latitude'], self.mock_latitude)
        self.assertEqual(self.mock_record['longitude'], self.mock_longitude)

    @patch.object(DatabaseHandler, "write_map_point")
    def test_record_map_point_calls_database_handler(self, mock_write_map_point):
        mock_write_map_point.return_value = None
        expected_args = {'date': int(self.mock_timestamp), 'lat':self.mock_latitude, 'long':self.mock_longitude}

        self.test_listener.record_map_point(self.mock_latitude, self.mock_longitude, self.mock_timestamp)

        mock_write_map_point.assert_called_with(expected_args)

if __name__ == '__main__':
    unittest.main()