from pymongo import MongoClient
from bson.objectid import ObjectId


class DatabaseHandler:
        def __init__(self, user, passwd):
                self.client = MongoClient('ds061335.mongolab.com', 61335)
                self.db = self.client.flutracker
                self.db.authenticate(user, passwd)


        def write_english_tweet_to_database(self, record):
                self.db.english_tweets.insert(record)

        def write_non_english_tweets_to_database(self, record):
                self.db.non_english_tweets.insert(record)

        def write_map_point(self, record):
                self.db.map_points.insert(record)

        def get_map_points_for_five_dates(self, start, end):
                res = self.db.map_points.find({'date': {'$lt': int(start), '$gt': int(end)}})
                return res

        def get_map_point_data(self, max_lat, max_lng, min_lat, min_lng, start_date, end_date):
                start_date = int(start_date) + 1
                end_date = int(end_date) - 1

                res = self.db.map_points.find({'lat': {'$lt': float(max_lat), '$gt': float(min_lat)},
                                               'long': {'$lt': float(max_lng), '$gt': float(min_lng)},
                                               'date': {'$lt': start_date, '$gt': end_date}})
                return res

        def get_uncategorised_tweet_from_english_collection(self):
                res = self.db.english_tweets.find_one({'sentiment': 'unknown'})
                return res

        def update_document_sentiment_in_english_collection(self, id, sentiment, text):
                res = self.db.english_tweets.update_one(
                        {"_id": ObjectId(id)},
                        {"$set": {"sentiment": sentiment}}
                )
                res = self.db.english_tweets.find_one({"text": text, "id": id})
                return res

        def get_tweets_with_sentiment(self, sentiment):
                return self.db.english_tweets.find({'sentiment': sentiment}).limit(1400)

        def get_total_count(self):
                return self.db.english_tweets.find().count()

        def get_today_count(self, today_date):
                return self.db.english_tweets.find({'created': today_date}).count()

        def get_yearly_count(self, year):
                low = year + '01' + '00'
                high = year + '12' + '31'
                return self.db.english_tweets.find({'created': {'$lte': high, '$gte': low}}).count()

        def get_month_count(self, year_month):
                low = year_month + '01'
                high = year_month + '31'
                return self.db.english_tweets.find({'created': {'$lte': high, '$gte': low}}).count()

        def get_count_for_max_min_dates(self, max_date, min_date):
                count = self.db.english_tweets.find({'created': {'$gte': min_date, '$lte': max_date}}).count()
                return count

