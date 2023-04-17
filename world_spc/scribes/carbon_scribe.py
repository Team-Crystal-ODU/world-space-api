from flask import current_app
from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY
import random
import pytz


def analyze_fuels(fuels):
    total = sum(fuels.values())

    co2_per_wH = (((fuels['Coal']/total) * 2.23)
                  + ((fuels['Natural gas']/total) * 0.91)
                  + ((fuels['Petroleum']/total) * 2.13)) / 1000

    perc_from_fossil_fuels = (
        fuels['Natural gas'] + fuels['Coal'] + fuels['Petroleum']) / total

    return co2_per_wH, perc_from_fossil_fuels


def analyze_co2(grid_data, watt_hours, start: datetime, end: datetime):
    """
    Takes a dict of hourly grid samples and calculates
    the pounds CO2 per watt-hour. Start and end timestamps
    are used to calculate partial hours.

    Equal to %coal * 2.23 + %natgas * 0.91 + %petroleum * 2.13.
    """
    co2_total = 0
    wH_total = 0
    result = []

    for watts, fuels in zip(watt_hours, grid_data):
        watt_hours = (watts['total'] / watts['sample_count'])
        wH_total += watt_hours
        co2_per_wH, perc_from_fossil_fuels = analyze_fuels(fuels['megawatts'])
        co2 = co2_per_wH * watt_hours
        co2_total += co2
        result.append({
            'hour_ending': str(fuels['timestamp']),
            'average_watts': watt_hours,
            'perc_from_fossil_fuels': perc_from_fossil_fuels
        })

    return co2_total, wH_total, result


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

    for obj in query:
        obj.pop('_id')
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

    result = []

    for obj in query:
        obj.pop('_id')
        obj.pop('samples')
        result.append(obj)
    return result


def get_five_day_range():
    end = datetime(2023, 4, 16, 22, 35, 23)
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
    total_co2, total_wH, chart_data = analyze_co2(
        grid_data, watt_hours, start, end)

    # miles_driven = total_co2 / 0.77

    result = {}

    result.update({
        'start_time': str(start),
        'end_time': str(end),
        'co2': round(total_co2, 2),
        'watt_hours': round(total_wH, 2),
        'miles_driven': round((total_co2 / 0.77), 2),
        'ppm': random.randint(300, 400),
        'chart_data': chart_data
    })

    return result


def main():
    get_five_day_range()


if __name__ == "__main__":
    main()
