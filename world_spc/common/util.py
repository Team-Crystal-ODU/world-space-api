# use this file for helper functions common across API
from flask import current_app
import json
import os
from world_spc.scribes import carbon_scribe


def create_mock_payload():
    """
    Helper function for testing purposes. Loads and returns sample JSON
    taken from EIA grid data.
    """
    with open(
            os.path.join(current_app.instance_path, 'mock_raw_grid_data.json')
    ) as json_file:
        mock_payload = json.load(json_file)
    return mock_payload


def create_mock_game_state():
    """
    Helper to test game state interface.
    """
    state = {
        "ppm": 335,
        "currency": 2555,
        "xp": 23560
    }
    species_dict = {
        "fox": {
            "population": 20,
            "status": "OK"
        },
        "bluebird": {
            "population": 11,
            "status": "Struggling"
        },
        "bear": {
            "population": 8,
            "status": "Endangered"
        }
    }
    state.update({'species': species_dict})
    return state


def create_mock_carbon_readout():
    """
    Returns static readout for GUI hero space. For dev purposes
    only.
    """
    data = {}
    data.update({'username': 'ecogamer', 'ppm': 335})
    usage_dict = {
        'past24hours': {},
        'past10days': {}
    }
    data.update(usage_dict)
    return data


if __name__ == "__main__":
    print(create_mock_game_state())
