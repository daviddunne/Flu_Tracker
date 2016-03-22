import unittest
from unittest.mock import patch
from utilities.database_handler import DatabaseHandler
from bson.objectid import ObjectId
import collections


class DatabaseHandlerTests(unittest.TestCase):
    def setUp(self):
        # test_dbh sets up a db on localhost
        self.test_dbh = DatabaseHandler()
        self.setup_test_dbh_initial_contents()

    def setup_test_dbh_initial_contents(self):
        self.setup_map_points_collection()
        self.setup_english_tweets_collection()
        self.setup_non_english_tweets_collection()

    def setup_map_points_collection(self):
        # clear previous test records  [ CAUTION CHECK THAT DB OS NOT PRODUCTION DB ]
        self.test_dbh.db.map_points.remove()
        # write initial test_records
        for num in range(1, 4):  # loops for 3 months
            for num_of_rec in (1, num + 1):  # mth1 gets 1 rec, mth2 gets 2, mth3 gets 3 etc
                record = {'date': int('20160' + str(num_of_rec) + '01'), 'lat': '000000', 'long': '000000',
                          'text': "test_text" + str(num_of_rec)}
                self.test_dbh.db.map_points.insert(record)

    def setup_english_tweets_collection(self):
        # clear previous test records  [ CAUTION CHECK THAT DB OS NOT PRODUCTION DB ]
        self.test_dbh.db.english_tweets.remove()
        # write initial test_records
        for num in range(1, 4):  # loops for 3 months
            for num_of_rec in (1, num + 1):  # mth1 gets 1 rec, mth2 gets 2, mth3 gets 3 etc
                record = {'created': '20160' + str(num_of_rec) + '01', 'user_language': 'en',
                          'address': 'test address', 'latitude': '000000', 'longitude': '000000'}
                self.test_dbh.db.english_tweets.insert(record)

    def setup_non_english_tweets_collection(self):
        # clear previous test records   [ CAUTION CHECK THAT DB OS NOT PRODUCTION DB ]
        self.test_dbh.db.non_english_tweets.remove()
        # write initial test_records
        for num in range(1, 4):  # loops for 3 months
            for num_of_rec in (1, num + 1):
                record = {'created': '20160' + str(num_of_rec) + '01', 'user_language': 'pt',
                          'address': 'test address', 'latitude': '000000', 'longitude': '000000'}
                self.test_dbh.db.non_english_tweets.insert(record)

    def test_write_english_tweet_to_database_writes_record_to_test_db_english_tweet_table(self):
        # Arrange
        initial_collection_count = 6
        record = {'created': int('20160102'), 'user_language': 'en',
                  'address': 'test address', 'latitude': '000000', 'longitude': '000000'}

        # Execute
        self.test_dbh.write_english_tweet_to_database(record)

        # Check
        self.assertEqual(initial_collection_count + 1, self.test_dbh.db.english_tweets.find().count())
        self.assertEqual(record, self.test_dbh.db.english_tweets.find_one({'created': 20160102}))

    def test_write_non_english_tweets_to_database_writes_record_to_test_db(self):
        initial_collection_count = 6
        record = {'created': int('20160102'), 'user_language': 'pt',
                  'address': 'test address', 'latitude': '000000', 'longitude': '000000'}

        # Execute
        self.test_dbh.write_non_english_tweets_to_database(record)

        # Check
        self.assertEqual(initial_collection_count + 1, self.test_dbh.db.non_english_tweets.find().count())
        self.assertEqual(record, self.test_dbh.db.non_english_tweets.find_one({'created': 20160102}))

    def test_write_map_point_writes_record_to_test_db(self):
        initial_collection_count = 6
        record = {'date': '20160102', 'lat': '000000', 'long': '000000',
                          'text': "test_text entered by write_method"}

        # Execute
        self.test_dbh.write_map_point(record)

        # Check
        self.assertEqual(initial_collection_count + 1, self.test_dbh.db.map_points.find().count())
        self.assertEqual(record, self.test_dbh.db.map_points.find_one({'date': '20160102'}))

    def test_get_map_points_for_five_dates_returns_points_for_five_days(self):
        # Arrange
        expected_count = 3

        # Execute
        points = self.test_dbh.get_map_points_for_five_dates('20160105', '20160101')

        # Check
        self.assertEqual(expected_count, points.count())

    def test_get_map_point_data_returns_points_within_defined_area(self):
        # Arrange
        record = {'date': int('20160601'), 'lat': 53.3478, 'long': 6.2597,
                  'text': "test_text"}
        self.test_dbh.db.map_points.insert(record)
        expected_count = 1

        # Execute
        records = self.test_dbh.get_map_point_data('54','52', '7', '5', '20160605', '20160531')

        # Check
        self.assertEqual(expected_count, records.count())

    def test_get_uncategorised_tweet_from_english_collection_returns_uncategorised_tweet(self):
        # Arrange
        record = {'created': '20160101', 'user_language': 'en', 'address': 'test address',
                  'latitude': '000000', 'longitude': '000000', 'sentiment': 'unknown'}
        self.test_dbh.db.english_tweets.insert(record)

        # Execute
        record = self.test_dbh.get_uncategorised_tweet_from_english_collection()

        # Check
        self.assertEqual('unknown', record['sentiment'])

    def test_update_document_sentiment_in_english_collection_updates_document(self):
        # Arrange
        record = {'created': '20160101', 'user_language': 'en', 'address': 'test address',
                  'latitude': '000000', 'longitude': '000000', 'sentiment': 'unknown'}
        record_id = self.test_dbh.db.english_tweets.insert(record) # returns id of newly created record
        expected_modified_count = 1

        modified_count = self.test_dbh.update_document_sentiment_in_english_collection(record_id, 'hasFlu',
                                                                                       'sample_text')
        # retrieve record to check sentiment
        record = self.test_dbh.db.english_tweets.find_one({"_id": ObjectId(record_id)})

        # Check
        self.assertEqual(expected_modified_count, modified_count)
        self.assertEqual('hasFlu', record['sentiment'])

    def test_get_tweets_with_sentiment_returns_appropriate_records(self):
        # Arrange
        record = {'created': '20160101', 'user_language': 'en', 'address': 'test address',
                  'latitude': '000000', 'longitude': '000000', 'sentiment': 'unknown'}
        self.test_dbh.db.english_tweets.insert(record)

        # Execute
        records = self.test_dbh.get_tweets_with_sentiment('unknown')

        # Check
        self.assertEqual(1, records.count())

    def test_get_total_count_returns_total_count(self):
        # Arrange
        expected_total_count = 6

        # Check
        self.assertEqual(expected_total_count, self.test_dbh.get_total_count())

    def test_get_today_count_return_todays_count(self):
        # Arrange
        expected_today_count = 3

        # Check
        self.assertEqual(expected_today_count, self.test_dbh.get_today_count('20160101'))

    def test_get_yearly_count_returns_year_count(self):
        # Arrange
        expected_yearly_count = 6

        # Check
        self.assertEqual(expected_yearly_count, self.test_dbh.get_yearly_count('2016'))

    def test_get_month_count_returns_month_count(self):
        # Arrange
        expected_count = 3

        # Check
        self.assertEqual(expected_count, self.test_dbh.get_month_count('201601'))

    def test_get_count_for_time_period_returns_correct_count_for_time_period(self):
        self.assertEqual(3, self.test_dbh.get_count_for_time_period('20160101', '20160101'))

    @patch('graphs.date_ranges.get_date_ranges_for_this_year')
    def test_get_instance_count_for_each_week_of_this_year_returns_dict_containing_correct_counts(self, test_patch):
        # Arrange
        test_patch.return_value = {'week0': {'start_date': '20151228', 'end_date': '20160103'}}
        expected_results = collections.OrderedDict([('0', 3)])

        # Check
        self.assertEqual(expected_results,
                         self.test_dbh.get_instance_count_for_each_week_of_this_year())
