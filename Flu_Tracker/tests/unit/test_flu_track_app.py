import unittest
import unittest.mock
from unittest.mock import Mock
from flu_track_app import app
import flu_track_app
from flask import json
import collections
import datetime



class FlaskAppTester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.dbh_mock = Mock()
        self.datetime_mock = Mock()

        self.setup_mock_responses()

        flu_track_app.database_handler = self.dbh_mock
        flu_track_app.weekly_data_retriever = self.dbh_mock
        flu_track_app.datetime = self.datetime_mock

    def setup_mock_responses(self):
        self.dbh_mock.get_map_points_for_five_dates.return_value = [dict(lat="testlat", long='testlong')]
        self.dbh_mock.get_uncategorised_tweet_from_english_collection.return_value = {"text": "test text", "_id": 1}
        self.dbh_mock.update_document_sentiment_in_english_collection.return_value = 1
        self.dbh_mock.get_today_count.return_value = 1
        self.dbh_mock.get_month_count.return_value = 2
        self.dbh_mock.get_yearly_count.return_value = 3
        self.dbh_mock.get_total_count.return_value = 4
        self.dbh_mock.get_instance_count_count_for_each_week_of_this_year.return_value = \
            collections.OrderedDict([('0', 1), ('1', 2),('10', 11), ('2', 3), ('3', 4), ('4', 5),
                                     ('5', 6), ('6', 7), ('7', 8), ('8', 9), ('9', 10)])
        self.dbh_mock.get_map_point_data.return_value = [{'lat': 0, 'long': 0, 'date': '01012016', 'text': "test text"}]
        self.datetime_mock.now.return_value = datetime.datetime.strptime('2016-01-05 00:00:00.000001',
                                                                         '%Y-%m-%d %H:%M:%S.%f')

    def test_get_request_to_root_returns_response_data_containing_FluTrakr_html_template(self):
        expected_in_response = '<title>Flu-Trakr</title>'

        response = self.app.get('/')

        self.assertTrue(expected_in_response in response.data.decode("utf-8"))

    def test_get_request_to_getuncategorisedtweet_endpoint_returns_correct_response(self):

        # self.dbh_mock.get_uncategorised_tweet_from_english_collection.return_value = {"text": "test text", "_id": 1}

        response = self.app.get('/getuncategorisedtweet')
        data = json.loads(response.data)['results']

        self.assertEqual(data['text'], 'test text')
        self.assertEqual(data['id'], '1')

    def test_get_request_to_getuncategorisedtweet_endpoint_returns__error_message_when_keyerror_raised(self):
        expected_response_text = "NO TWEET AVAILABLE, PLEASE REFRESH"
        # Overwrite the response value for the mock to suit this test
        self.dbh_mock.get_uncategorised_tweet_from_english_collection.return_value = {}

        response = self.app.get('/getuncategorisedtweet')
        data = json.loads(response.data)['results']

        self.assertEqual(data['id'], None)
        self.assertEqual(data['text'], expected_response_text)

    def test_put_request_to_update_tweet_sentiment_endpoint_calls_database_update_script_with_correct_params(self):
        request_params = dict(id=1, sentiment='hasflu', text='I have the flu')

        self.app.put('/update/tweet/sentiment', data=request_params)

        self.dbh_mock.update_document_sentiment_in_english_collection.assert_called_with('1',
                                                                                         'hasflu',
                                                                                         'I have the flu')

    def test_get_request_to_get_stats_count_endpoint_executes_db_query_get_today_count_with_correct_date(self):
        request_params = dict(day=11, month=22, year=3333)

        self.app.get('/get/stats/count', data=request_params)

        self.dbh_mock.get_today_count.assert_called_with("33332211")

    def test_get_request_toget_stats_count_endpoint_executes_db_query_get_month_count_with_correct_year_and_month(self):
        request_params = dict(day=11, month=22, year=3333)

        self.app.get('/get/stats/count', data=request_params)

        self.dbh_mock.get_month_count.assert_called_with("333322")

    def test_get_request_to_get_stats_count_endpoint_executes_db_query_get_yearly_count_with_correct_year(self):
        request_params = dict(day=11, month=22, year=3333)

        self.app.get('/get/stats/count', data=request_params)

        self.dbh_mock.get_yearly_count.assert_called_with("3333")

    def test_get_request_to_get_stats_count_endpoint_returns_expected_results(self):

        request_params = dict(day=11, month=22, year=3333)

        response = self.app.get('/get/stats/count', data=request_params)
        json_data = json.loads(response.data)['results']

        self.assertEqual(json_data['today'], 1)
        self.assertEqual(json_data['month'], 2)
        self.assertEqual(json_data['year'], 3)
        self.assertEqual(json_data['all'], 4)

    # def test_get_request_to_get_weekly_chart_data_returns_expected_results(self):
    #     expected_results = {'results': {'data': {'6': 7, '2': 3, '5': 6, '7': 8, '1': 2, '8': 9, '10': 11,
    #                                              '9': 10, '3': 4, '4': 5, '0': 1}}}
    #     response = self.app.get('/get/weekly/chart/data')
    #     response_data = json.loads(response.data)
    #     self.assertEqual(expected_results, response_data)

    def test_get_request_to_get_data_points_for_area_returns_expected_results(self):
        expected_results = {'data': [{'long': 0, 'text': 'test text', 'date': '01012016', 'lat': 0}]}
        request_params = dict(lat=-1, lng=-1, start_date='2016-01-01', end_date='2016-01-02')

        response = self.app.get('/get/data/points/for/area', data=request_params)

        self.assertEqual(expected_results, json.loads(response.data))

    def test_get_request_to_get_data_points_for_area_returns_unknown_text_when_text_not_present(self):
        expected_results = {'data': [{'long': 0, 'text': 'Unknown', 'date': '01012016', 'lat': 0}]}
        request_params = dict(lat=-1, lng=-1 ,start_date='2016-01-01', end_date='2016-01-02')
        self.dbh_mock.get_map_point_data.return_value = [{'lat': 0, 'long': 0, 'date': '01012016'}]

        response = self.app.get('/get/data/points/for/area', data=request_params)

        self.assertEqual(expected_results, json.loads(response.data))

    def test_setup_dates_for_query_returns_five_day_period_from_today_when_number_from_scrollbar_is_one(self):
        expected_start = 20160105
        expected_end = 20160101
        start, end = flu_track_app.setup_dates_for_query(1)

        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_setup_dates_for_query_returns_five_day_period_from_today_when_number_from_scrollbar_is_not_one(self):
        expected_start = 20160104
        expected_end = 20151231

        start, end = flu_track_app.setup_dates_for_query(2)

        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_normalise_date_returns_expected_results_when_fed_string_of_length_eight(self):
        expected_result = "2016-01-01"

        normalised_date = flu_track_app.normalise_date("20160101")

        self.assertEqual(expected_result, normalised_date)

    def test_normalise_date_returns_expected_results_when_fed_string_of_length_seven(self):
        expected_result = "2016-01-01"

        normalised_date = flu_track_app.normalise_date("2016011")

        self.assertEqual(expected_result, normalised_date)

    def test_normalise_date_returns_expected_results_when_fed_string_of_length_six(self):
        expected_result = "2016-01-01"

        normalised_date = flu_track_app.normalise_date("201611")

        self.assertEqual(expected_result, normalised_date)

if __name__ == '__main__':
    unittest.main()
