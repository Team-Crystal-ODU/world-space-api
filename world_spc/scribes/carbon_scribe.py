import json
from flask import current_app
from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY


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
    pass


def get_watt_hours_over_interval(start: datetime, end: datetime, user, db):
    """
    Retrieve user watt-hours over a specified interval.
    """
    pass


def get_five_day_range():
    end = datetime(2023, 2, 20, 22, 35, 23)
    start = end - timedelta(days=5)
    # print(f'start={datetime.strftime(start, "%Y-%m-%dT%H:%M:%S")}')
    # print(f'end={datetime.strftime(end, "%Y-%m-%dT%H:%M:%S")}')
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

    total_CO2 = watt_hours * co2_per_wh
    miles_driven = total_CO2 / 0.77

    result = {}

    return result


def main():
    pass


if __name__ == "__main__":
    main()
