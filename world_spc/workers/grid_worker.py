import json
import os
from flask import current_app


def parse_raw_data(raw_data):
    pass


if __name__ == "__main__":
    result = {}
    with open('mock_raw_grid_data.json') as json_file:
        raw_data = json.load(json_file)
        generation_data = raw_data['series'][:]
        result.update({'timestamp': raw_data['series'][0]['data'][-1]['Timestamp (Hour Ending)']})
        result.update({'megawatts': {}})
        print(result)

        for elem in generation_data:
            source = elem['name']
            latest_hour = elem['data'][-1]
            result['megawatts'].update({source: latest_hour['value']})
        print(result)

