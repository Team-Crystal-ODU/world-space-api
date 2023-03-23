from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY
from flask import current_app
import json


def generate(db):
    # TODO intelligently construct start and end dates by parsing data
    start_date = datetime(2023, 2, 14, 0)
    end_date = datetime(2023, 2, 20, 0)

    # Build a list of hours based on the overall span of grid data
    # to be parsed.
    hours = [timestamp for timestamp in rrule(
        HOURLY, dtstart=start_date, until=end_date
    )]

    with current_app.open_resource('mocking/mock_raw_grid_data.json') as f:
        raw_data = json.load(f)
        generation_data = raw_data['series'][:]
        fuels = []
        col = db['grid']
        for i, elem in enumerate(generation_data):
            fuels.append(generation_data[i]['name'])
        for i, hour in enumerate(hours):
            bucket = {}
            bucket.update({
                'region': 'mida',
                'data': []
            })
            bucket.update(
                {
                    'timestamp': format_timestamp(
                        generation_data[0]
                        ['data'][i]['Timestamp (Hour Ending)']
                    ),
                    'megawatts': {}
                }
            )
            for j, fuel in enumerate(fuels):
                bucket['megawatts'].update(
                    {
                        fuel: int(generation_data[j]['data'][i]['value'])
                    }
                )
            col.insert_one(bucket)


def format_timestamp(unformatted):
    """
    Takes the timestamp value from the EIA grid data and formats it
    for insertion into MongoDB. Date is separated from time. Time
    stored as integer (0-23) for hour-ending, where 0 corresponds to
    midnight.
    Args: The unformatted timestamp string.
    Yields: A list of the form [date: str, time: int, timezone: str]
    """
    parts = unformatted.split(' ')
    # format date part
    date_part = datetime.strptime(parts[0], '%m/%d/%Y')

    # format time part
    if parts[2] == 'a.m.':
        parts[1] = ' '.join((parts[1], 'AM'))
    else:
        parts[1] = ' '.join((parts[1], 'PM'))
    time_part = datetime.strptime(parts[1], '%I %p')
    formatted = ''.join((date_part.strftime('%Y-%m-%dT'),
                        time_part.strftime('%H:%M:%S')))
    return formatted


if __name__ == "__main__":
    generate()
