#   Author: David Dunne,    Student Number: C00173649, Created Jan 2016

import unittest
from unittest.mock import patch
from unittest.mock import Mock
from utilities.geolocation_finder import GeolocationFinder
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


class GeolocationFinderTests(unittest.TestCase):
    def setUp(self):
        self.test_geolocation_finder = GeolocationFinder()
        self.setup_mocks()

    def setup_mocks(self):
        self.attrs = {'address': 'test_address', 'latitude': '0000', 'longitude': '0000'}
        self.test_geolocation = Mock(**self.attrs)
        self.test_geolocation_finder.geolocation = Mock(**self.attrs)

    def test_GetLocation_ReturnsNoneNoneNone_IfLocationIsNone(self):
        # Checks
        self.assertEqual((None, None, None), self.test_geolocation_finder.get_location(None))

    def test_get_location_sets_geolocation_from_cache_When_geolocation_exists_in_cache(self):
        # Arrange
        self.test_geolocation_finder.location_cache['Dublin'] = self.test_geolocation

        # Execute
        with patch.object(GeolocationFinder, 'set_geolocation_from_cache') as mock_method:
            self.test_geolocation_finder.get_location('Dublin')

        # Checks
        mock_method.assert_called_once_with('Dublin')

    def test_get_location_sets_geolocation_from_geolocator_when_not_present_in_cache(self):

        # Execute
        with patch.object(GeolocationFinder, 'set_geolocation_from_geolocator',
                          return_value=self.test_geolocation) as mock_method:
            self.test_geolocation_finder.get_location('Dublin')

        # Checks
        mock_method.assert_called_once_with('Dublin')

    def test_get_location_sets_geolocation_from_geolocator_adds_geolocation_to_cache(self):
        # Arrange
        self.test_geolocation_finder.location_cache = {}

        # Execute
        with patch.object(Nominatim, 'geocode', return_value=self.test_geolocation) as mock_method:
            self.test_geolocation_finder.get_location('Dublin')

        # Checks
        self.assertTrue('Dublin' in self.test_geolocation_finder.location_cache)

    def test_set_geolocation_from_cache_sets_the_geolocation(self):
        # Arrange
        self.test_geolocation_finder.location_cache['Dublin'] = self.test_geolocation

        # Execute
        self.test_geolocation_finder.set_geolocation_from_cache('Dublin')

        # Checks
        self.assertEqual(self.test_geolocation_finder.geolocation, self.test_geolocation)

    def test_set_geolocation_from_geolocator_sets_geolocation(self):

        # Execute
        with patch.object(Nominatim, 'geocode', return_value=self.test_geolocation):
            self.test_geolocation_finder.set_geolocation_from_geolocator('Dublin')

        # Checks
        self.assertEqual(self.test_geolocation_finder.geolocation, self.test_geolocation)

    def test_set_geolocation_from_geolocator_sets_geolocation_to_None_when_GeocoderTimedOut_exception_raised(self):

        # Execute
        with patch.object(Nominatim, 'geocode', side_effect=GeocoderTimedOut):
            self.test_geolocation_finder.set_geolocation_from_geolocator('Dublin')

        # Checks
        self.assertEqual(self.test_geolocation_finder.geolocation, None)

    def test_get_addr_lat_long_raises_AttributeError_and_returns_None_None_None_when_no_geolocation_passed(self):
        # Arrange
        self.test_geolocation_finder.geolocation = None

        # Execute
        address, lat, long = self.test_geolocation_finder.get_addr_lat_long()

        # Checks
        self.assertEqual(address, None)
        self.assertEqual(lat, None)
        self.assertEqual(long, None)

    def test_get_addr_lat_long(self):

        # Execute
        address, lat, long = self.test_geolocation_finder.get_addr_lat_long()

        # Checks
        self.assertEqual(address, 'test_address')
        self.assertEqual(lat, '0000')
        self.assertEqual(long, '0000')


if __name__ == '__main__':
    unittest.main()