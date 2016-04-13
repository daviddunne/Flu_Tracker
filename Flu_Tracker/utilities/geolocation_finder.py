#   Author: David Dunne,    Student Number: C00173649,      Created Nov 2015

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges
from geolocation.main import GoogleMaps
from utilities import logger
google_map_api_key = "AIzaSyBEPT7qp4ex_7lxyT9OMk3-UhC8rC5rabU"


class GeolocationFinder:
    """
    Class for retrieving geolocation when given an address.
    Class creates a cache of geolocations to minimise calls to geopy library, reducing the risk of hitting rate limit
    """
    def __init__(self):
        self.location_cache = {}
        self.geolocator = Nominatim()
        self.geolocation = None
        self.backup_geolocator = GoogleMaps(api_key=google_map_api_key)
        self.lat = None
        self.long = None

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
            if self.geolocation is not None or self.lat is not None:
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
        self.geolocation = None
        self.lat = None
        self.long = None

        try:
            self.geolocation = self.geolocator.geocode(location, timeout=None)
        except GeocoderTimedOut:
            logger.logging.warning('GeolocationFinder: geolocator timeout')
            print("geologger timeout")
        except GeocoderUnavailable:
            print("geologger unavailable")
        except GeocoderInsufficientPrivileges:
            # geopy doesnt work: go to backup geolocation finder
            logger.logging.error("GeolocationFinder: Geocoder insufficient privileges")
            self.getGeolocationInfoFromBackupGeolocator(location)
        if self.geolocation is not None:
            self.location_cache[location] = self.geolocation

    def getGeolocationInfoFromBackupGeolocator(self, location):
        try:
            google_geolocation = self.backup_geolocator.search(location=location)
            loc = google_geolocation.first()
            self.lat = loc.lat
            self.long = loc.lng
            self.address = location
        except:
            self.geolocation = None

    def get_addr_lat_long(self):
        """
        Gets address, latitude, longitude from the class geolocation attribute
        :return: address:string, latitude:float, longitude:float
        """
        try:
            if self.geolocation is None:
                address = self.address
                latitude = self.lat
                longitude = self.long
            else:
                address = self.geolocation.address
                latitude = self.geolocation.latitude
                longitude = self.geolocation.longitude
        except AttributeError:
            logger.logging.exception('Attribute Error:GeolocationFinder.get_addr_lat_long in geolocation_finder')
            address, latitude, longitude = None, None, None
        self.geolocation = None
        return address, latitude, longitude
