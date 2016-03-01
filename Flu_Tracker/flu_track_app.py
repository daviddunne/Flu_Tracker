from flask import Flask, render_template, request, jsonify, make_response
from utilities.database_handler import DatabaseHandler
from graphs.graph_data import WeeklyDataRetriever
from datetime import datetime, timedelta


app = Flask(__name__)
database_handler = DatabaseHandler('flutrackapp', 'flutrackapp')
wdr = WeeklyDataRetriever('datagrapher', 'datagrapher')


@app.route('/', methods=['GET'])
def default_page():
    return render_template('home.html')


@app.route('/getmappoints', methods=['POST'])
def get_map_points():
    number_from_scrollbar = request.values.get('time', type=int)
    start_date, end_date = setup_dates_for_query(number_from_scrollbar)

    # Execute Query
    result = database_handler.get_map_points_for_five_dates(start_date, end_date)

    points = get_points_from_result(result)
    # Normalise dates for display
    start_date -= 1
    end_date +=1
    start_date = normalise_date(str(start_date))
    end_date = normalise_date(str(end_date))
    values = {"datapoints": points, "start_date": start_date, "end_date": end_date}

    return jsonify(results=values)


@app.route('/categorise')
def categorise():
    return render_template('dataCategorisor.html')


@app.route('/getuncategorisedtweet', methods=['GET'])
def get_uncatagorised_tweet():
    result = database_handler.get_uncategorised_tweet_from_english_collection()
    try:
        text = result['text']
        id = str(result['_id'])
        values = {"text": text, "id": id}
    except TypeError:
        values = {"text": "NO TWEET AVAILABLE, PLEASE REFRESH", 'id': None}

    return jsonify(results=values)


@app.route('/update/tweet/sentiment', methods=['PUT'])
def update_tweet_sentiment():
    id = str(request.values.get('id'))
    sentiment = request.values.get('sentiment', type=str)
    text = request.values.get('text', type=str)
    result = database_handler.update_document_sentiment_in_english_collection(id, sentiment, text)
    updated_tweets = result.modified_count
    values = {'count': updated_tweets}
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
    data = wdr.get_graph_data_for_weekly_chart()
    values = {'data': data}
    return make_response(jsonify(results=values), 200)


@app.route('/get/data/points/for/area', methods=['GET'])
def get_data_points_for_area():
    days_of_tweets = 4

    # Define the radius for tweets on clicking of map
    max_lat = request.values.get('max_lat')
    min_lat = request.values.get('min_lat')
    max_lng = request.values.get('max_lng')
    min_lng = request.values.get('min_lng')
    start_date = (request.values.get('start_date')).replace('-','')
    end_date = (request.values.get('end_date')).replace('-', '')
    data = database_handler.get_map_point_data(max_lat, max_lng, min_lat, min_lng, start_date, end_date)

    points = []
    for record in data:
        point = {}
        point['lat'] = record['lat']
        point['long'] = record['long']
        point['date'] = record['date']
        try:
            point['text'] = record['text']
        except KeyError:
            point['text'] = 'Unknown'
        points.append(point)

    values = {'data': points}
    return jsonify(values)


def get_points_from_result(result):
    points = []
    for record in result:
        point = [record['lat'], record['long']]
        points.append(point)

    return points


def setup_dates_for_query(number_from_scrollbar):
    date_format = "%Y%m%d"
    start_date, end_date = setup_days(number_from_scrollbar)
    todays_date = datetime.now()
    # Get date for query
    start = (todays_date - timedelta(start_date)).strftime(date_format)
    end = (todays_date - timedelta(end_date)).strftime(date_format)
    start = int(start) + 1
    end = int(end) - 1
    return start, end


def setup_days(number_from_scrollbar):
    if number_from_scrollbar < 3:
        start = 0
        end = 5
    else:
        start = number_from_scrollbar - 2
        end = number_from_scrollbar + 3
    return start, end


def normalise_date(date):
    # Normalise date
    # If is less than 8 characters i.e. 1012015, change to 01012015
    if len(date) < 8:
        date = '0' + str(date)
    # Date now must change from 01012015 to 01-01-2015
    date = date[:4] + '-' + date[4:6] + '-' + date[6:]

    return date


if __name__ == '__main__':
    app.run(debug=True)
