from flask import Flask, render_template, request, jsonify, make_response
from utilities.database_handler import DatabaseHandler
from datetime import datetime, timedelta


app = Flask(__name__)

database_handler = DatabaseHandler('ds061335.mongolab.com', 61335, 'flutrackapp', 'flutrackapp')



@app.route('/', methods=['GET'])
def default_page():
    return render_template('home.html')


@app.route('/getmappoints', methods=['GET'])
def get_map_points():
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


@app.route('/categorise', methods=['GET'])
def categorise():
    return render_template('dataCategorisor.html')


@app.route('/getuncategorisedtweet', methods=['GET'])
def get_uncatagorised_tweet():
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
    id = str(request.values.get('id'))
    sentiment = request.values.get('sentiment', type=str)
    text = request.values.get('text', type=str)
    updated_count = database_handler.update_document_sentiment_in_english_collection(id, sentiment, text)
    values = {'count': updated_count}

    return jsonify(results=values)


@app.route('/get/stats/count', methods=['GET'])
def get_stats_counts():
    day = str(request.values.get('day'))
    month = str(request.values.get('month'))
    year = str(request.values.get('year'))
    date = year+month+day
    day_count = database_handler.get_today_count(date)
    year_count = database_handler.get_yearly_count(year)
    month_count = database_handler.get_month_count(year + month)
    all_time_count = database_handler.get_total_count()
    values = {'all': all_time_count, 'year': year_count, 'month': month_count, 'today': day_count}

    return jsonify(results=values)


@app.route('/get/weekly/chart/data', methods=['GET'])
def get_weekly_chart_date():
    data = database_handler.get_instance_count_for_each_week_of_this_year()
    values = {'data': data}

    return make_response(jsonify(results=values), 200)


@app.route('/get/data/points/for/area', methods=['GET'])
def get_data_points_for_area():
    """
    Retrieves map points from database within a specified area and date range
    :return: list of map point records
    """
    # Define the area and date ranges for database query
    max_lat, max_lng, min_lat, min_lng, start_date, end_date = define_parameters_for_get_map_point_data_database_query()
    # Query the database
    query_result = database_handler.get_map_point_data(max_lat, max_lng, min_lat, min_lng, start_date, end_date)
    # Extract the points from the query
    points = extract_points_from_query_result(query_result)
    values = {'data': points}

    return jsonify(values)


def define_parameters_for_get_map_point_data_database_query():
    """
    Generates the query arguments required to get text from all tweets within a 50km square of map click and
    within date range specified on a scrollbar
    :param: none
    :returns: maximum latitude, maximum Longitude, minimum latitude, minimum longitude, start date, end date
    """
    fifty_km = 0.5
    lat = request.values.get('lat')
    lng = request.values.get('lng')

    max_lat = float(lat) + fifty_km
    min_lat = float(lat) - fifty_km
    max_lng = float(lng) + fifty_km
    min_lng = float(lng) - fifty_km
    start_date = (request.values.get('start_date')).replace('-', '')
    end_date = (request.values.get('end_date')).replace('-', '')

    return max_lat, max_lng, min_lat, min_lng, start_date, end_date


def extract_points_from_query_result(data):
    points = []
    for record in data:
        point = {'lat': record['lat'], 'long': record['long'], 'date': record['date']}
        try:
            point['text'] = record['text']
        except KeyError:
            point['text'] = 'Unknown'
        points.append(point)

    return points


def get_lats_and_longs_from_query_result(result):
    points = []
    for record in result:
        point = [record['lat'], record['long']]
        points.append(point)

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


def normalise_date(date):
    # Normalise date Date must change from 01012015 to 01-01-2015
    # If is less than 8 characters i.e. 1012015, change to 01012015
    if len(date) == 7:
        date = date[:4] + '-' + date[4:6] + '-0' + date[6:]
    elif len(date) == 6:
        date = date[:4] + '-0' + date[4:5] + '-0' + date[5:]
    else:
        date = date[:4] + '-' + date[4:6] + '-' + date[6:]

    return date

app.secret_key = 'Youwillneverguess'

if __name__ == '__main__':
    app.run(debug=True)
