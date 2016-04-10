from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.error import TweepError
from tweepy.streaming import StreamListener
import json
import datetime
import time
import logging
from utilities.database_handler import DatabaseHandler
from utilities.validator import ValidatorClass
from utilities import logger
from utilities.geolocation_finder import GeolocationFinder


# Set authentication variables
ckey = '3q6FL0iOlqjbCFWmstT7xozQo'
csecret = '5OoEe1jXDwAB65wkgR9lG4wJkq19dWcA2CogAfmOl4l0w2VH7m'
atoken = '2915745407-Iuj5hcqjaKyeSiqMzhwpqdo6YUsGM0EHkp58XpM'
asecret = 'Vcu5Kupvl6BEOdNiWDkQc2hQX8LhVzkqjp444gMFJNOKG'

# Relative path to pickle files
pathToPickleFiles = 'classifiers/pickle_files/'

# DB Credentials
dbURL = 'ds061335.mongolab.com'
dbPort = 61335
dbUser = 'datacollector'
dbPasswd = 'datacollector'
# Words to listen for
keyword_list = ['manflu', 'flu']


class DataCollector(StreamListener):
    def __init__(self):
        self.validator = ValidatorClass(pathToPickleFiles)
        self.geo_finder = GeolocationFinder()
        self.database_handler = DatabaseHandler(dbURL, dbPort,dbUser, dbPasswd)

    def on_data(self, raw_data):
        # Load the raw data
        try:
            json_data = json.loads(raw_data)

            # Get some required details from json data
            user_id, text, language, location, timestamp = self.get_data_from_json_data(json_data)

            # Check if text in tweet is valid before processing
            if text != 'invalid' and self.validator.validate_text_from_tweet(text):
                record = {'created': timestamp, 'user_language': language}

                # Check if tweet contains a valid location
                if self.validator.validate_location(location) and location != 'None':
                    # get location details of user
                    address, latitude, longitude = self.geo_finder.get_location(location)

                    # If location has not returned None for lat and long, construct and record the map point in database
                    if (latitude is not None) and (longitude is not None) \
                            and (latitude != 'None') and (longitude != 'None'):
                        self.add_to_record(address, latitude, longitude, record)
                        self.record_map_point(latitude, longitude, timestamp, text)
                # Check if language is english
                if self.language_is_english(language):
                    self.database_handler.write_english_tweet_to_database(record)
        except TypeError:
            logger.logging.exception('Error during on_data method')
        except ValueError:
            logger.logging.exception('Error during on_data method')

    def language_is_english(self, language):
        return (language == 'en') or (language == 'en-gb')

    def add_to_record(self, address, latitude, longitude, record):
        # Add location values to record
        record['address'] = address
        record['latitude'] = latitude
        record['longitude'] = longitude

    def record_map_point(self, latitude, longitude, timestamp, text):
        map_point_record = {'date': int(timestamp), 'lat': latitude, 'long': longitude, 'text': text}
        self.database_handler.write_map_point_to_database(map_point_record)

    def get_data_from_json_data(self, json_data):
        try:
            user_id = json_data['user']['id_str']

        except KeyError:
            logger.logging.exception('KeyError while accessing user ID')
            user_id = 'unknown'
        try:
            user_language = json_data['user']['lang']
        except KeyError:
            logger.logging.exception('KeyError while accessing user language')
            user_language = 'unknown'
        try:
            loc = json_data['user']['location']
        except KeyError:
            logger.logging.exception('KeyError while accessing user location')
            loc = None
        try:
            text = json_data['text'].lower()
        except KeyError:
            # if keyError is raised set the text to a banned word so it will not be accepted
            text = 'invalid text'
            logger.logging.exception('KeyError while accessing tweet text')
        # Get time tweet picked up
        timestamp = self.get_timestamp()

        return user_id, text, user_language, loc, timestamp

    def get_timestamp(self):
        now = datetime.datetime.now()
        day = str(now.day)
        month = str(now.month)
        year = str(now.year)

        if len(day) == 1:
            day = '0' + day
        if len(month) == 1:
            month = '0' + month
        timestamp = year + month + day
        return timestamp

    def on_error(self, status_code):
        logging.error('Twitter Stream returned status code:')


def runDataCollector():
    # Authenticate and connect to twitter
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, DataCollector())
    print('Starting Data Collector Process')
    try:
        # DataCollector to capture data containing keywords
        twitterStream.filter(track=keyword_list)
    except TweepError as e:
        logger.logging.critical("Critical error from Twitter Stream")
        # Wait 5 seconds and attempt to restart DataCollector
        i = 5
        print('Error during data collection, attempting to restart in:')
        while i > 0:
            print(str(i))
            i -= 1
            time.sleep(1)
        twitterStream.filter(track=keyword_list)
    except Exception as e:
        print('Unknown exception occurred when running tweepy')
        logger.logging.critical('Unknown exception occurred when running tweepy')

if __name__ == '__main__':
    runDataCollector()

