from utilities.database_handler import DatabaseHandler
from graphs.date_ranges import get_date_ranges_for_this_year
import collections


class WeeklyDataRetriever:
    def __init__(self, user, passwd):
        self.dbh = DatabaseHandler('datagrapher', 'datagrapher')

    def get_graph_data_for_weekly_chart(self):

        # Gets the start and end daes for each week of the year
        date_ranges = get_date_ranges_for_this_year()

        # Create an ordered dictionary of weekly counts
        count_date_dict = {}
        for key, value in date_ranges.items():
            count_date_dict[key.replace('week', '')] = self.dbh.get_count_for_max_min_dates(value['end_date'], value['start_date'])
        count_date_dict = collections.OrderedDict(sorted(count_date_dict.items()))

        return count_date_dict
