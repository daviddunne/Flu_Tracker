#   Author: David Dunne,    Student Number: C00173649,      Created Nov 2015

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from utilities import logger


class GeolocationFinder:
    """
    Class for retrieving geolocation when given an address.
    Class creates a cache of geolocations to minimise calls to geopy library, reducing the risk of hitting rate limit
    """
    def __init__(self):
        self.location_cache = {}
        self.geolocator = Nominatim()
        self.geolocation = None

    def get_location(self, location):
        """
        gets location attributes give a location
        :param location: string
        :return: address:string, latitude:float, longitude:float
        """
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
        """
        sets class geolocation attribute to geolocation from the cache
        :param location: string
        """
        self.geolocation = self.location_cache[location]

    def set_geolocation_from_geolocator(self, location):
        """
        Sets class geolocation attribute to geolocation from the geopy library and adds new eolocation to cache
        :param location: string
        """
        try:
            self.geolocation = self.geolocator.geocode(location, timeout=None)
        except GeocoderTimedOut:
            logger.logging.warning('GeolocationFinder: geolocator timeout')
            self.geolocation = None
        except GeocoderUnavailable:
            self.geolocation = None
        if self.geolocation is not None:
            self.location_cache[location] = self.geolocation

    def get_addr_lat_long(self):
        """
        Gets address, latitude, longitude from the class geolocation attribute
        :return: address:string, latitude:float, longitude:float
        """
        try:
            address = self.geolocation.address
            latitude = self.geolocation.latitude
            longitude = self.geolocation.longitude
        except AttributeError:
            logger.logging.exception('Attribute Error:GeolocationFinder.get_addr_lat_long in geolocation_finder')
            address, latitude, longitude = None, None, None
        self.geolocation = None
        return address, latitude, longitude
