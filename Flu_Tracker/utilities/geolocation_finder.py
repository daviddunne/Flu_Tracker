from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from utilities import logger


class GeolocationFinder:
    def __init__(self):
        self.location_cache = {}
        self.geolocator = Nominatim()
        self.geolocation = None

    def get_location(self, location):
            if location is None:
                    return None, None, None
            elif location in self.location_cache:
                # Check cache for location
                self.set_geolocation_from_cache(location)
                address, latitude, longitude = self.get_addr_lat_long()
                return address, latitude, longitude
            else:
                # Location not cached so fetch from geolocator
                self.set_geolocation_from_geolocator(location)
                if self.geolocation is not None:
                    address, latitude, longitude = self.get_addr_lat_long()
                    return address, latitude, longitude
                return None, None, None

    def set_geolocation_from_cache(self, location):
        self.geolocation = self.location_cache[location]

    def set_geolocation_from_geolocator(self, location):
        try:
            self.geolocation = self.geolocator.geocode(location, timeout=None)
        except GeocoderTimedOut:
            logger.logging.warning('GeolocationFinder: geolocator timeout')
            self.geolocation = None
        if self.geolocation is not None:
            self.location_cache[location] = self.geolocation

    def get_addr_lat_long(self):
        try:
            address = self.geolocation.address
            latitude = self.geolocation.latitude
            longitude = self.geolocation.longitude
        except AttributeError:
            logger.logging.warning('GeolocationFinder: Attribute Error occurred during execution of get_addr_lat_long in geolocation_finder')
            address, latitude, longitude = None, None, None
        self.geolocation = None
        return address, latitude, longitude

