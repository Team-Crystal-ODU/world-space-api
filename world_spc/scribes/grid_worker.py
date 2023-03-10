import json
import os
from flask import current_app
from datetime import datetime


def parse_latest():
    result = {}
    with open(
        os.path.join(
            current_app.instance_path,
            'mock_raw_grid_data.json'
        )
    ) as json_file:
        raw_data = json.load(json_file)
        generation_data = raw_data['series'][:]
        result.update({
            'timestamp':
                format_timestamp(
                    raw_data['series'][0]['data']
                    [-1]['Timestamp (Hour Ending)']
                )
            })
        result.update({'megawatts': retrieve_hour(generation_data)})
    return result


def retrieve_hour(data):
    result = {}
    for elem in data:
        source = elem['name']
        latest_hour = elem['data'][-1]
        result.update({source: latest_hour['value']})
    return result


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
    result = parse_latest()
    print(result)
