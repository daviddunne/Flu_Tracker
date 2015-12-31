from pymongo import MongoClient


class DatabaseHandler:
        def __init__(self):
                self.client = MongoClient()
                self.db = self.client.flu_tracker

        def write_english_tweet_to_database(self, record):
                self.db.english_tweets.insert(record)

        def write_non_english_tweets_to_database(self, record):
                self.db.non_english_tweets.insert(record)

        def write_map_point(self, record):
                self.db.map_points.insert(record)

        def get_map_points_for_five_dates(self, one, two, three, four, five):
                res = self.db.map_points.find({"date": one, "date": two,"date": three,"date": four,"date": five})
                return res
