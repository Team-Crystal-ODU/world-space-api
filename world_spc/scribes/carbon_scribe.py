import json
from flask import current_app
from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY


def get_carbon_readout(user, db):
    start, end = get_five_day_range()


def get_CO2_perc_over_interval(start: datetime, end: datetime):
    pass


def get_watt_hours_over_interval(start: datetime, end: datetime):
    pass


def get_five_day_range():
    end = datetime(2023, 2, 20, 22, 35, 23)
    start = end - timedelta(days=5)
    print(f'start={datetime.strftime(start, "%Y-%m-%dT%H:%M:%S")}')
    print(f'end={datetime.strftime(end, "%Y-%m-%dT%H:%M:%S")}')
    return start, end


def main():
    pass


if __name__ == "__main__":
    main()
