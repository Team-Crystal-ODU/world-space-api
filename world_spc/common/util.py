# use this file for helper functions common across API
from flask import current_app
import json
import os

def create_mock_payload():
    """
    Helper function for testing purposes. Loads and returns sample JSON taken from EIA grid data.
    """
    with open(os.path.join(current_app.instance_path, 'mock_raw_grid_data.json')) as json_file:
        mock_payload = json.load(json_file)
    return mock_payload