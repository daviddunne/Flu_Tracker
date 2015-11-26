from __future__ import print_function
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime
import json
from geopy.geocoders import Nominatim

geolocator = Nominatim()

# Set authentication variables
ckey = '3q6FL0iOlqjbCFWmstT7xozQo'
csecret = '5OoEe1jXDwAB65wkgR9lG4wJkq19dWcA2CogAfmOl4l0w2VH7m'
atoken = '2915745407-Iuj5hcqjaKyeSiqMzhwpqdo6YUsGM0EHkp58XpM'
asecret = 'Vcu5Kupvl6BEOdNiWDkQc2hQX8LhVzkqjp444gMFJNOKG'
file_prefix = 'data/tweets_file_'
location_dict = {}

class Listener(StreamListener):
    def on_data(self, raw_data):
        banned = False
        json_data = json.loads(raw_data)
        text = json.loads(raw_data)['text']

        if self.banned_tweet(text):
             self.write_to_file('data/banned.json', raw_data)
        else:
            file_postfix = str(datetime.now().strftime('%Y:%m:%d')) + '.csv'
            data_file = file_prefix + file_postfix
            loc = json_data['user']['location']
            if loc != None:
                if loc in location_dict:
                    latlong = location_dict[loc]
                else:
                    latlong = self.get_lat_long(loc)
                if latlong != 'unknown':
                    timestamp = json_data['created_at']
                    user_id = json_data['user']['id_str']
                    location_dict[loc] = latlong
                    data = timestamp + ', ' + user_id + ', ' + loc + ', ' + text + ', ' + str(latlong[0]) + ', ' + str(latlong[1])
                    print(data)
                    self.write_to_file(data_file, data)

    def on_error(self, status_code):
        print(status_code)

    def get_lat_long(self, location):
        if location in location_dict:
            latlong = location_dict[location]
            return latlong
        else:
            if (location)== None:
                return 'unknown'
            else:
                loc = geolocator.geocode(location)
                try:
                    latlong = (loc.latitude, loc.longitude)
                    return latlong
                except AttributeError:
                    return 'unknown'

    def banned_tweet(self, text):
        banned = False
        for words in banned_list:
            if words in text:
                banned = True
                break
        return banned

    def write_to_file(self, path_to_file, input_data):
        with open(path_to_file, 'a') as output_file:
                output_file.write(input_data)

# Authenticate and connect to twitter
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, Listener())
keyword_list = ['this flu', 'manflu', 'have the flu', 'flu']
banned_list = ['shot','jab', 'rt', 'vaccinate', 'vaccine', 'vaccination' 'one direction', 'fda', 'https', '@', 'the priest thinks']

# Filter to capture data containing keywords
twitterStream.filter(track= keyword_list)

