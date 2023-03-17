from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY
from world_spc.scribes.grid_worker import format_timestamp
from flask import current_app
import json


def generate(db):
    # TODO intelligently construct start and end dates by parsing data
    start_date = datetime(2023, 2, 14, 0)
    end_date = datetime(2023, 2, 20, 0)

    # Build a list of hours based on the overall span of grid data
    # to be parse.
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


if __name__ == "__main__":
    generate()
