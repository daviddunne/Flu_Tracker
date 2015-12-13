from __future__ import print_function
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim()

# Set authentication variables
ckey = '3q6FL0iOlqjbCFWmstT7xozQo'
csecret = '5OoEe1jXDwAB65wkgR9lG4wJkq19dWcA2CogAfmOl4l0w2VH7m'
atoken = '2915745407-Iuj5hcqjaKyeSiqMzhwpqdo6YUsGM0EHkp58XpM'
asecret = 'Vcu5Kupvl6BEOdNiWDkQc2hQX8LhVzkqjp444gMFJNOKG'
file_prefix = 'data/tweets_file_'
location_cache = {}


class Listener(StreamListener):

    banned_word_list = ['stomach', 'rt ', 'one direction', 'https', '@', 'the priest thinks']

    def on_data(self, raw_data):
        to_data_file = self.set_up_data_file()
        json_data = json.loads(raw_data)
        location, text, user_language = self.get_location_text_and_user_language_from_data(json_data)

        # Check is tweet is valid, english and does not contain banned words
        if self.valid_tweet(location, text, user_language) and location != 'None':
        #ToDo remove location from validation check later add tweets with no location to database
            # get geolocation object of user
            geolocation = self.get_geolocation(location)
            #ToDo check if losing data here when geolocation is returning None
            if geolocation != None:
                address = geolocation.address
                latitude = geolocation.latitude
                longitude= geolocation.longitude

                # Get time tweet created
                timestamp = json_data['created_at']
                user_id = json_data['user']['id_str']

                # Cache the location for later use
                location_cache[location] = geolocation
                data = timestamp + ', ' + user_id + ', ' + text + ', ' + address + ', ' + str(latitude) + ', ' + str(longitude)
                #ToDo remove this print function before deploying
                print(data)
                #ToDo Refactor this code to add to database not file and include time so can perform queries for up to date data
                mapPoint = "\tnew google.maps.LatLng(" + str(latitude) + ", " + str(longitude) + "),"
                datafilepath = "static/js/mapDayPoints.js"
                file = open(datafilepath)
                lines = file.readlines()
                file.close()
                lines = lines[:-1]
                lines.append(mapPoint)
                lines.append('\n];')
                with open(datafilepath, 'w') as datafile:
                    datafile.writelines([item for item in lines])
                self.write(data, to_data_file)

    def set_up_data_file(self):
        # Set up data file
        file_postfix = str(datetime.now().strftime('%Y:%m:%d')) + '.csv'
        to_data_file = file_prefix + file_postfix
        return to_data_file

    def get_location_text_and_user_language_from_data(self, json_data):
        try:
            user_language = json_data['user']['lang']
        except KeyError:
            user_language = 'unknown'
        try:
            loc = json_data['user']['location']
        except KeyError:
            loc = None
        try:
            text = json_data['text'].lower()
        except KeyError:
            # if keyerror is raised set the text to a banned word so it will not be accepted
            text = 'shot'
        return loc, text, user_language

    def on_error(self, status_code):
        print(status_code)

    # Gets the geocode object of a location from the dictionary, if not present adds to location
    def get_geolocation(self, location):

        # Check cache for location
        if location in location_cache:
            geolocation = location_cache[location]
            return geolocation
        else:
            if (location)== None:
                return None
            else:
                # location not cached so fetch from geolocator
                try:
                    geolocation = geolocator.geocode(location, timeout=None)
                    location_cache[location] = geolocation
                    return geolocation
                except GeocoderTimedOut as e:
                    print('error Timeout')
                    return None
                except:
                    return None

    # Check a tweet is valid
    def valid_tweet(self, location, text, user_lang):
        if location is None:
            return False
        if user_lang != 'en':
            return False
        if text == '':
            return False
        for words in self.banned_word_list:
            if words in text:
                return False
        return True

    # Write data to a specified file
    def write(self, input_data, path_to_file):
        with open(path_to_file, 'a') as output_file:
                output_file.write(input_data)


if __name__ == '__main__':
    # Authenticate and connect to twitter
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, Listener())
    keyword_list = ['manflu', 'flu']


    # Filter to capture data containing keywords
    twitterStream.filter(track=keyword_list)
