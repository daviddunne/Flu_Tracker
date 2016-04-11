#   Author: David Dunne,    Student Number: C00173649,      Created Nov 2015

from pymongo import MongoClient
from bson.objectid import ObjectId
import collections

testDatabaseURL = 'localhost'
find_limit = 1400


class DatabaseHandler:
        def __init__(self, url='localhost', port=27017, user='', passwd=''):
                """
                Handles writes and queries to the Mongo Database
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
                if url != testDatabaseURL:
                        self.db.authenticate(user, passwd)

        def write_english_tweet_to_database(self, record):
                """
                Writes an english tweet record to english tweet collection in database
                :param record:
                :return: nothing
                """
                self.db.english_tweets.insert(record)

        def write_map_point_to_database(self, record):
                """
                Writes a map point record to map point collection in database
                :param record:
                :return: nothing
                """
                self.db.map_points.insert(record)

        def get_map_points_for_five_dates(self, start, end):
                """
                Retrieves all records from map points collection created from "start" to "end" inclusive
                :param start: string
                :param end: string
                :return: pymongo.cursor.Cursor containing records if there exists any
                """
                res = self.db.map_points.find({'date': {'$lte': int(start), '$gte': int(end)}})
                print(type(res))
                return res

        def get_map_point_data(self, max_lat, max_lng, min_lat, min_lng, start_date, end_date):
                """
                Retrieves all records that meet the criteria set out by the parameters
                :param max_lat: string
                :param max_lng: string
                :param min_lat: string
                :param min_lng: string
                :param start_date: string
                :param end_date: string
                :return: pymongo.cursor.Cursor containing records if there exists any
                """
                res = self.db.map_points.find({'lat': {'$lte': float(max_lat), '$gte': float(min_lat)},
                                               'long': {'$lte': float(max_lng), '$gte': float(min_lng)},
                                               'date': {'$lte': int(start_date), '$gte': int(end_date)}})
                return res

        def get_uncategorised_tweet_from_english_collection(self):
                """
                Used when developing a training set of tweets to get a record from
                english tweet collection with sentiment labelled unknown
                :return: pymongo.cursor.Cursor containing one record if there exists one
                """
                res = self.db.english_tweets.find_one({'sentiment': 'unknown'})
                return res

        def update_document_sentiment_in_english_collection(self, id, sentiment, text):
                """
                Used when developing a training set of tweets to relabel record with appropriate sentiment label
                :param id: string
                :param sentiment: string
                :param text: string
                :return: modified_count: int
                """
                res = self.db.english_tweets.update_one(
                        {"_id": ObjectId(id)},
                        {"$set": {"sentiment": sentiment}}
                )
                return res.modified_count

        def get_tweets_with_sentiment(self, sentiment):
                """
                Used for training classifiers to retrieve records from english tweets collection
                :param sentiment: string
                :return: pymongo.cursor.Cursor containing records if there exists any
                """
                return self.db.english_tweets.find({'sentiment': sentiment}).limit(find_limit)

        def get_total_count(self):
                """
                Used to retrieve data for statistics
                Retrieves the total number of records currently in english tweet collection
                :return: count: int
                """
                return self.db.english_tweets.find().count()

        def get_today_count(self, today_date):
                """
                Used to retrieve data for statistics
                Retrieves the number of records currently in english tweet collection created on date specified
                :param today_date: string
                :return: count: int
                """
                return self.db.english_tweets.find({'created': today_date}).count()

        def get_yearly_count(self, year):
                """
                Used to retrieve data for statistics
                Retrieves the number of records currently in english tweet collection created in year specified
                :param year: string
                :return: count: int
                """
                low = str(year) + '01' + '00'
                high = str(year) + '12' + '31'
                return self.db.english_tweets.find({'created': {'$lte': high, '$gte': low}}).count()

        def get_month_count(self, year_month):
                """
                Used to retrieve data for statistics
                Retrieves the number of records currently in english tweet collection created in
                month and year specified
                :param year_month: string
                :return: count: int
                """
                low = year_month + '01'
                high = year_month + '31'
                return self.db.english_tweets.find({'created': {'$lte': high, '$gte': low}}).count()

        def get_count_for_time_period(self, max_date, min_date):
                """
                Used to retrieve data for statistics (weekly map data)
                Retrieves the number of records currently in english tweet collection created between
                max_date and min_date inclusively
                :param max_date: string
                :param min_date: string
                :return: count: int
                """
                count = self.db.english_tweets.find({'created': {'$lte': max_date, '$gte': min_date}}).count()
                return count

        def get_instance_count_for_each_week_of_this_year(self, date_range):
                """
                Takes the date range dictionary, gets count for each week contained, adds them to ordered dictionary
                :param date_range: Dictionary containing this years week numbers mapped to their start and end dates
                :return: count_date_dict: Dictionary containing this years week numbers mapped to their record count
                """
                # Create an ordered dictionary of weekly counts
                count_date_dict = {}
                for label, value in date_range.items():
                    count_date_dict[label.replace('week', '')] = self.get_count_for_time_period(value['end_date'], value['start_date'])
                count_date_dict = collections.OrderedDict(sorted(count_date_dict.items()))
                return count_date_dict
