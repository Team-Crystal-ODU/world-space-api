from flask import current_app
from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY
from bson.json_util import dumps, loads
import pytz


def get_CO2_per_watt_hour(grid_data: dict, start: datetime, end: datetime):
    """
    Takes a dict of hourly grid samples and calculates
    the pounds CO2 per watt-hour. Start and end timestamps
    are used to calculate partial hours.

    Equal to %coal * 2.23 + %natgas * 0.91 + %petroleum * 2.13.
    """
    pass


def get_grid_data(start: datetime, end: datetime, db):
    """
    Retrieve hourly grid data inclusive of the specified
    start and end times.
    """
    delta = timedelta(hours=1)
    est = pytz.timezone('US/Eastern')

    first_hour = datetime(start.year, start.month,
                          start.day, start.hour) + delta
    last_hour = datetime(end.year, end.month,
                         end.day, end.hour) + delta
    query = db.grid.find({
        'timestamp': {'$gte': est.localize(first_hour),
                      '$lte': est.localize(last_hour)}
    })

    result = []
    # naive tz adjustment, because localize not working as expected
    # for string output
    tz = timedelta(hours=5)

    for obj in query:
        obj.pop('_id')
        obj['timestamp'] = obj['timestamp'] - tz
        obj['timestamp'] = str(obj['timestamp'])
        result.append(obj)

    return result


def get_watt_hours_over_interval(start: datetime, end: datetime, user, db):
    """
    Retrieve user watt-hours over a specified interval.
    """
    est = pytz.timezone('US/Eastern')
    query = db.ecogamer.find({
        'end_time': {'$gte': est.localize(start),
                     '$lte': est.localize(end)}
    })

    query_as_list = list(query)
    result = dumps(query_as_list)

    return result


def get_five_day_range():
    end = datetime(2023, 2, 20, 22, 35, 23)
    start = end - timedelta(days=5)
    return start, end


def get_fuel_breakdown(grid_data: dict):
    pass


def get_miles_driven(co2):
    pass


def get_carbon_readout(user, db):
    start, end = get_five_day_range()
    watt_hours = get_watt_hours_over_interval(start, end, user, db)
    grid_data = get_grid_data(start, end, db)
    co2_per_wh = get_CO2_per_watt_hour(grid_data, start, end)

    #total_CO2 = watt_hours * co2_per_wh
    #miles_driven = total_CO2 / 0.77

    result = {}

    result.update({
        'watt-hours': watt_hours
    })

    return result


def main():
    get_five_day_range()


if __name__ == "__main__":
    main()
