#   Author: David Dunne,    Student Number: C00173649,      Created Nov 2015

from flask import Flask, render_template, request, jsonify, make_response
from utilities.database_handler import DatabaseHandler
from datetime import date, datetime, timedelta


app = Flask(__name__)

database_handler = DatabaseHandler('ds061335.mongolab.com', 61335, 'flutrackapp', 'flutrackapp')


@app.route('/', methods=['GET'])
def default_page():
    """
    Renders web interface for flu-TrakR
    :return: rendered html page
    """
    return render_template('home.html')


@app.route('/categorise', methods=['GET'])
def categorise():
    """
    Used to render form for labelling sentiment of tweets for purposes of developing a training set
    :return: rendered html page containing web form
    """
    return render_template('dataCategorisor.html')


@app.route('/getmappoints', methods=['GET'])
def get_map_points():
    """
    Retrieves map points from map point collection in database that were created in a 5 day period within
    the last month specified by user
    :return: dictionary containing points, start date and end date
    """
    number_from_scrollbar = request.values.get('time', type=int)
    start_date, end_date = setup_dates_for_query(number_from_scrollbar)

    # Execute Query
    result = database_handler.get_map_points_for_five_dates(start_date, end_date)
    # Extract points from query result
    points = get_lats_and_longs_from_query_result(result)
    # Normalise dates for display
    start_date = normalise_date(str(start_date))
    end_date = normalise_date(str(end_date))
    values = {"datapoints": points, "start_date": start_date, "end_date": end_date}

    return jsonify(results=values)


@app.route('/getuncategorisedtweet', methods=['GET'])
def get_uncatagorised_tweet():
    """
    API endpoint for getting a single uncategorised record from the english tweet collection
    restricted to a get method to prevent overwriting of record in db
    :return: dictionary containing text and id of uncategorised record retrieved from english tweet collection
    """
    result = database_handler.get_uncategorised_tweet_from_english_collection()
    try:
        text = result['text']
        tweet_id = str(result['_id'])
        values = {"text": text, "id": tweet_id}
    except (TypeError, KeyError):
        values = {"text": "NO TWEET AVAILABLE, PLEASE REFRESH", 'id': None}

    return jsonify(results=values)


@app.route('/update/tweet/sentiment', methods=['PUT'])
def update_tweet_sentiment():
    """
    API endpoint for updating the sentiment of a specified record from the english tweet collection
    :return: dictionary containing updated count
    """
    # Get params from the request data
    record_id = str(request.values.get('id'))
    sentiment = request.values.get('sentiment', type=str)
    text = request.values.get('text', type=str)
    # Send query
    updated_count = database_handler.update_document_sentiment_in_english_collection(record_id, sentiment, text)
    values = {'count': updated_count}

    return jsonify(results=values)


@app.route('/get/stats/count', methods=['GET'])
def get_stats_counts():
    """
    API endpoint for getting counts for current day, month, year and all time
    :return: Dictionary containing count for "all", "year", "month" and "today"
    """
    # Get params from the request data
    day = str(request.values.get('day'))
    month = str(request.values.get('month'))
    year = str(request.values.get('year'))
    # Send queries
    day_count = database_handler.get_today_count(year+month+day)
    month_count = database_handler.get_month_count(year + month)
    year_count = database_handler.get_yearly_count(year)
    all_time_count = database_handler.get_total_count()
    values = {'all': all_time_count, 'year': year_count, 'month': month_count, 'today': day_count}

    return jsonify(results=values)


@app.route('/get/weekly/chart/data', methods=['GET'])
def get_weekly_chart_date():
    """
    API endpoint for retrieving counts for each week of the current year
    :return: Dictionary containing counts for each week of the current year
    """
    # Get the start and end dates for each week of this year
    date_ranges = get_date_ranges_for_this_year()
    data = database_handler.get_instance_count_for_each_week_of_this_year(date_ranges)
    values = {'data': data}

    return make_response(jsonify(results=values), 200)


@app.route('/get/data/points/for/area', methods=['GET'])
def get_data_points_for_area():
    """
    Retrieves map points from database within a specified area and date range
    :return: list of map point records
    """
    # Define the area and date ranges for database query
    max_lat, max_lng, min_lat, min_lng, start_date, end_date = define_params_database_query()
    # Query the database
    query_result = database_handler.get_map_point_data(max_lat, max_lng, min_lat, min_lng, start_date, end_date)
    # Extract the points from the query
    points = extract_points_from_query_result(query_result)
    values = {'data': points}

    return jsonify(values)


def define_params_database_query():
    """
    Generates the query arguments required to get text from all tweets within a 50km square of map click and
    within date range specified on a scrollbar
    :param: none
    :returns: maximum latitude, maximum Longitude, minimum latitude, minimum longitude, start date, end date
    """
    distance_range = 0.5
    lat = request.values.get('lat')
    lng = request.values.get('lng')

    max_lat = float(lat) + distance_range
    min_lat = float(lat) - distance_range
    max_lng = float(lng) + distance_range
    min_lng = float(lng) - distance_range
    start_date = (request.values.get('start_date')).replace('-', '')
    end_date = (request.values.get('end_date')).replace('-', '')

    return max_lat, max_lng, min_lat, min_lng, start_date, end_date


def extract_points_from_query_result(data):
    """
    Creates a list of dictionaries containing 'lat', 'long' and 'text'
    :param data:
    :return:
    """
    points = []
    for record in data:
        point = {'lat': record['lat'], 'long': record['long'], 'date': record['date']}
        # Try here as text was not stored when app was launched so there exists some records without text
        try:
            point['text'] = record['text']
        except KeyError:
            point['text'] = 'Unknown'
        points.append(point)

    return points


def get_lats_and_longs_from_query_result(result):
    """
    Creates a list of lists containing lats and longs
    :param result:
    :return: points: List<List<string>>
    """
    points = []
    for record in result:
        try:
            point = [record['lat'], record['long']]
            points.append(point)
        except KeyError:
            pass
    return points


def setup_dates_for_query(number_from_scrollbar):
    """
    Sets up a date range in relation to the position of time filter scrollbar.
    Range between start and end date should always be five days.
    :param number_from_scrollbar:
    :return: start date and end date
    """
    date_format = "%Y%m%d"
    if number_from_scrollbar == 1:
        start = 0
        end = 4
    else:
        start = number_from_scrollbar - 1
        end = number_from_scrollbar + 3
    # Get date for query
    today_date = datetime.now()
    start = (today_date - timedelta(start)).strftime(date_format)
    end = (today_date - timedelta(end)).strftime(date_format)
    start = int(start)
    end = int(end)

    return start, end


def normalise_date(in_date):
    """
    Changes date format to desired one
    e.g. from 01012015 to 01-01-2015, if date less than 8 characters i.e. 1012015, change to 01012015
    :param in_date: string
    :return: date: string
    """
    if len(in_date) == 7:
        in_date = in_date[:4] + '-' + in_date[4:6] + '-0' + in_date[6:]
    elif len(in_date) == 6:
        in_date = in_date[:4] + '-0' + in_date[4:5] + '-0' + in_date[5:]
    else:
        in_date = in_date[:4] + '-' + in_date[4:6] + '-' + in_date[6:]

    return in_date


def get_date_ranges_for_this_year():
    """
    Gets the start and end dates for each week of the current year
    :return: Dictionary containing week numbers mapped to start and end dates
    """
    today = date.today()
    current_week = today.isocalendar()[1]
    week_dict = {}
    week = 0
    while week <= current_week:
            start = get_week_start_date(2016, week)
            end = start + timedelta(days=6)
            start = start.strftime('%Y%m%d')
            end = end.strftime('%Y%m%d')
            week_dict["week" + str(week)] = {"start_date": start, "end_date": end}
            week += 1
    return week_dict


def get_week_start_date(year, week):
    """
    gets the date of the beginning on a week given a year and week number
    :param year: int
    :param week: int
    :return: date
    """
    d = date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta

app.secret_key = 'Youwillneverguess'

if __name__ == '__main__':
    app.run(debug=True)
