import unittest
from unittest.mock import patch
from unittest.mock import Mock
from utilities.geolocation_finder import GeolocationFinder
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


class GeolocationFinderTests(unittest.TestCase):
    def setUp(self):
        self.test_geolocation_finder = GeolocationFinder()
        self.attrs = {'address': 'test_address', 'latitude': '0000', 'longitude': '0000'}

    def test_GetLocation_ReturnsNoneNoneNone_IfLocationIsNone(self):

        self.assertEqual((None, None, None), self.test_geolocation_finder.get_location(None))

    def test_get_location_sets_geolocation_from_cache_When_geolocation_exists_in_cache(self):
        # Arrange
        test_geolocation = Mock(**self.attrs)
        self.test_geolocation_finder.location_cache['Dublin'] = test_geolocation

        # Execute
        with patch.object(GeolocationFinder, 'set_geolocation_from_cache') as mock_method:
            self.test_geolocation_finder.get_location('Dublin')

        # Check
        mock_method.assert_called_once_with('Dublin')

    def test_get_location_sets_geolocation_from_geolocator_when_not_present_in_cache(self):
        # Arrange
        test_geolocation = Mock(**self.attrs)

        with patch.object(GeolocationFinder, 'set_geolocation_from_geolocator',
                          return_value=test_geolocation) as mock_method:
            # Execute
            self.test_geolocation_finder.get_location('Dublin')
        # Check
        mock_method.assert_called_once_with('Dublin')

    def test_get_location_sets_geolocation_from_geolocator_adds_geolocation_to_cache(self):
        # Arrange
        test_geolocation = Mock(**self.attrs)
        self.test_geolocation_finder.location_cache = {}

        # Execute
        with patch.object(Nominatim, 'geocode', return_value=test_geolocation) as mock_method:
            self.test_geolocation_finder.get_location('Dublin')

        # Check
        self.assertTrue('Dublin' in self.test_geolocation_finder.location_cache)

    def test_set_geolocation_from_cache_sets_the_geolocation(self):
        # Arrange
        test_geolocation = Mock(**self.attrs)
        self.test_geolocation_finder.location_cache['Dublin'] = test_geolocation

        # Execute
        self.test_geolocation_finder.set_geolocation_from_cache('Dublin')

        # Check
        self.assertEqual(self.test_geolocation_finder.geolocation, test_geolocation)

    def test_set_geolocation_from_geolocator_sets_geolocation(self):
        # Arrange
        test_geolocation = Mock(**self.attrs)

        # Execute
        with patch.object(Nominatim, 'geocode', return_value=test_geolocation):
            self.test_geolocation_finder.set_geolocation_from_geolocator('Dublin')

        self.assertEqual(self.test_geolocation_finder.geolocation, test_geolocation)

    def test_set_geolocation_from_geolocator_sets_geolocation_to_None_when_GeocoderTimedOut_exception_raised(self):

        with patch.object(Nominatim, 'geocode', side_effect=GeocoderTimedOut):
            self.test_geolocation_finder.set_geolocation_from_geolocator('Dublin')

        self.assertEqual(self.test_geolocation_finder.geolocation, None)

    def test_get_addr_lat_long_raises_AttributeError_and_returns_None_None_None_when_no_geolocation_passed(self):
        # Arrange
        self.test_geolocation_finder.geolocation = None

        # Execute
        address, lat, long = self.test_geolocation_finder.get_addr_lat_long()
        self.assertEqual(address, None)
        self.assertEqual(lat, None)
        self.assertEqual(long, None)

    def test_get_addr_lat_long(self):

        self.test_geolocation_finder.geolocation = Mock(**self.attrs)
        address, lat, long = self.test_geolocation_finder.get_addr_lat_long()

        self.assertEqual(address, 'test_address')
        self.assertEqual(lat, '0000')
        self.assertEqual(long, '0000')


if __name__ == '__main__':
    unittest.main()