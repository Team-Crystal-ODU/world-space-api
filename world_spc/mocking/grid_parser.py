from datetime import datetime
from dateutil.rrule import rrule, HOURLY
from world_spc.scribes.grid_worker import format_timestamp
import json


def main():
    # TODO intelligently construct start and end dates by parsing data
    start_date = datetime(2023, 2, 14, 0)
    end_date = datetime(2023, 2, 20, 0)

    bucket = {}
    bucket.update({'region': 'mida'})
    bucket.update({'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S')})
    bucket.update({'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S')})
    bucket.update({'data': []})

    print(bucket)

    hours = [timestamp for timestamp in rrule(
        HOURLY, dtstart=start_date, until=end_date
    )]

    with open('mock_raw_grid_data.json') as f:
        raw_data = json.load(f)
        generation_data = raw_data['series'][:]
        fuels = []
        for i, elem in enumerate(generation_data):
            fuels.append(generation_data[i]['name'])
        for i, hour in enumerate(hours):
            bucket['data'].append(
                {
                    'timestamp': format_timestamp(
                        generation_data[0]
                        ['data'][i]['Timestamp (Hour Ending)']
                    ),
                    'megawatts': {}
                }
            )
            for j, fuel in enumerate(fuels):
                bucket['data'][i]['megawatts'].update(
                    {
                        fuel: int(generation_data[j]['data'][i]['value'])
                    }
                )
        result = json.dumps(bucket, indent=4)

    with open('mock_formatted_grid_data.json', 'w') as outfile:
        outfile.write(result)


if __name__ == "__main__":
    main()
