from flask import Flask, render_template, request, jsonify
from utilities.database_handler import DatabaseHandler
from datetime import datetime, timedelta

app = Flask(__name__)
database_handler = DatabaseHandler()


@app.route('/', methods=['GET'])
def default_page():
    return render_template('home.html')


@app.route('/getmappoints', methods=['POST'])
def get_map_points():
    number_from_scrollbar = request.values.get('time', type=int)
    day_five = number_from_scrollbar + 2
    day_four = number_from_scrollbar + 1
    day_three = number_from_scrollbar
    if number_from_scrollbar == 0:
        day_two = number_from_scrollbar
        day_one = number_from_scrollbar
    elif number_from_scrollbar == 1:
        day_one = number_from_scrollbar - 1
        day_two = number_from_scrollbar - 1
    else:
        day_two = number_from_scrollbar - 1
        day_one = number_from_scrollbar - 2
    # Get todays date
    todays_date = datetime.now()

     # Get date for query
    date_one = int((todays_date - timedelta(day_one)).strftime("%d%m%Y"))
    date_two = int((todays_date - timedelta(day_two)).strftime("%d%m%Y"))
    date_three = int((todays_date - timedelta(day_three)).strftime("%d%m%Y"))
    date_four = int((todays_date - timedelta(day_four)).strftime("%d%m%Y"))
    date_five = int((todays_date - timedelta(day_five)).strftime("%d%m%Y"))


    # Execute Query
    result = database_handler.get_map_points_for_five_dates(date_one, date_two, date_three, date_four, date_five)
    points = []
    for record in result:
        point = [record['lat'], record['long']]
        points.append(point)

    # Normalise dates for display
    start_date = normalise_date(str(date_one))
    end_date = normalise_date(str(date_five))

    values = {"datapoints": points, "start_date": start_date, "end_date": end_date}
    return jsonify(results=values)


def normalise_date(date):
    # Normalise date
    # If is less than 8 characters i.e. 1012015, change to 01012015
    if len(date) < 8:
        date = '0' + str(date)
    # Date now must change from 01012015 to 01-01-2015
    date = date[:2] + '-' + date[2:4] + '-' + date[4:]
    return date


if __name__ == '__main__':
    app.run(debug=True)
