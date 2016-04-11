#   Author: David Dunne,    Student Number: C00173649, Created March 2016

import unittest
from flu_track_app import app

# Response Codes
success_response_status_code = 200
method_not_allowed_status_code = 405


class FlaskAppTester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_root_endpoint_returns_success_for_get_request(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, success_response_status_code)

    def test_getmappoints_endpoint_returns_success_for_get_request_with_time_param_of_one(self):
        request_params = dict(time=1)
        response = self.app.get('/getmappoints', data=request_params)
        self.assertEqual(response.status_code, success_response_status_code)

    def test_categorise_endpoint_returns_success_for_get_request(self):
        response = self.app.get('/categorise')
        self.assertEqual(response.status_code, success_response_status_code)

    def test_get_stats_count_endpoint_returns_success_for_get_request(self):
        request_params = dict(day='20', month='03', year='2016')
        response = self.app.get('/get/stats/count', data=request_params)
        self.assertEqual(response.status_code, success_response_status_code)

    def test_get_weekly_chart_data_returns_success_for_get_request(self):
        response = self.app.get('/get/weekly/chart/data')
        self.assertEqual(response.status_code, success_response_status_code)

    def test_get_data_points_for_area_returns_success_for_get_request(self):
        request_params = dict(lat=53.3478, lng=6.2597, start_date='2016-03-23', end_date='2016-03-22')
        response = self.app.get('/get/data/points/for/area', data=request_params)
        self.assertEqual(response.status_code, success_response_status_code)
