from pymongo import MongoClient
from bson.objectid import ObjectId
from graphs import date_ranges
import collections


class DatabaseHandler:
        def __init__(self, url='localhost', port=27017, user='', passwd=''):
                """
                :param url: location of mongoDB host
                :param port: port for mongoDB
                :param user: username for database
                :param passwd: password for database
                :return: Database Handler Object instance
                """
                self.user = user
                self.passwd = passwd
                self.client = MongoClient(url, port)
                self.db = self.client.flutracker
                if url != "localhost":
                        self.db.authenticate(user, passwd)

        def write_english_tweet_to_database(self, record):
                self.db.english_tweets.insert(record)

        def write_non_english_tweets_to_database(self, record):
                self.db.non_english_tweets.insert(record)

        def write_map_point(self, record):
                self.db.map_points.insert(record)

        def get_map_points_for_five_dates(self, start, end):
                res = self.db.map_points.find({'date': {'$lte': int(start), '$gte': int(end)}})
                return res

        def get_map_point_data(self, max_lat, max_lng, min_lat, min_lng, start_date, end_date):

                res = self.db.map_points.find({'lat': {'$lte': float(max_lat), '$gte': float(min_lat)},
                                               'long': {'$lte': float(max_lng), '$gte': float(min_lng)},
                                               'date': {'$lte': int(start_date), '$gte': int(end_date)}})
                return res

        def get_uncategorised_tweet_from_english_collection(self):
                # Used when developing a training set of tweets.
                res = self.db.english_tweets.find_one({'sentiment': 'unknown'})
                return res

        def update_document_sentiment_in_english_collection(self, id, sentiment, text):
                # Used when developing a training set of tweets.

                res = self.db.english_tweets.update_one(
                        {"_id": ObjectId(id)},
                        {"$set": {"sentiment": sentiment}}
                )
                return res.modified_count

        def get_tweets_with_sentiment(self, sentiment):
                # Used for training classifiers
                return self.db.english_tweets.find({'sentiment': sentiment}).limit(1400)

        def get_total_count(self):
                return self.db.english_tweets.find().count()

        def get_today_count(self, today_date):
                print(type(today_date))
                return self.db.english_tweets.find({'created': today_date}).count()

        def get_yearly_count(self, year):
                # Used for statistics
                low = str(year) + '01' + '00'
                high = str(year) + '12' + '31'
                return self.db.english_tweets.find({'created': {'$lte': high, '$gte': low}}).count()

        def get_month_count(self, year_month):
                # Used for statistics
                low = year_month + '01'
                high = year_month + '31'
                return self.db.english_tweets.find({'created': {'$lte': high, '$gte': low}}).count()

        def get_count_for_time_period(self, max_date, min_date):
                # Used for statistics
                count = self.db.english_tweets.find({'created': {'$lte': max_date, '$gte': min_date}}).count()
                return count

        def get_instance_count_for_each_week_of_this_year(self):
                # Gets the start and end daes for each week of the year
                date_range = date_ranges.get_date_ranges_for_this_year()
                print(date_range)
                # Create an ordered dictionary of weekly counts
                count_date_dict = {}
                for label, value in date_range.items():
                    count_date_dict[label.replace('week', '')] = self.get_count_for_time_period(value['end_date'], value['start_date'])
                count_date_dict = collections.OrderedDict(sorted(count_date_dict.items()))

                return count_date_dict
