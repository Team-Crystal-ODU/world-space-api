import json
import os
from flask import current_app
from datetime import datetime
from dateutil.rrule import rrule, HOURLY
import requests


def update_grid_data(db, start):
    with open(os.path.join(current_app.instance_path, 'query')) as f:
        part1 = f.readline().strip()
        part2 = f.readline().strip()

    query = "".join((part1, start, part2))

    response = requests.get(query)
    payload = response.json()

    data = payload['response']['data']
    first_hour = datetime.strptime(data[-1]['period'], '%Y-%m-%dT%H')
    last_hour = datetime.strptime(data[0]['period'], '%Y-%m-%dT%H')

    hours = [time for time in rrule(
        HOURLY, dtstart=first_hour, until=last_hour
    )]

    col = db.grid

    grouped_by_hour = [[] for hour in hours]
    for idx, hour in enumerate(hours):
        search_value = hour.strftime('%Y-%m-%dT%H')
        for item in data:
            if search_value in item.values():
                grouped_by_hour[idx].append(item)

    for group in grouped_by_hour:
        time = datetime.strptime(group[0]['period'], '%Y-%m-%dT%H')
        q = col.count_documents({'timestamp': time})
        if q == 0:
            doc = {'region': 'mida', 'timestamp': time}
            megawatts = {}
            for entry in group:
                fuel = entry['type-name']
                value = entry['value']
                megawatts.update({fuel: value})
            doc.update({'megawatts': megawatts})
            col.insert_one(doc)

    return grouped_by_hour


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
    midnight. Only necessary for JSON downloaded via browser.
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
