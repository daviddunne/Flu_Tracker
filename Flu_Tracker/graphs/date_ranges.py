from datetime import date, timedelta


def get_date_ranges_for_this_year():
    today = date.today()
    week = today.isocalendar()[1]
    week_dict = {}
    current_week = 0
    while current_week <= week:
        start = get_week_start_date(2016, current_week)
        end = start + timedelta(days=6)
        start = start.strftime('%Y%m%d')
        end = end.strftime('%Y%m%d')
        week_dict["week" + str(current_week)] = {"start_date": start, "end_date": end}
        current_week += 1
    return week_dict


def get_week_start_date(year, week):
    d = date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    print(type(d + delta))
    return d + delta

