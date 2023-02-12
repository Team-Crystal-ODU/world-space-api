from flask_restful import Resource, fields, reqparse, marshal_with
from flask import current_app
import json
import os

# TODO investigate use of Pydantic for data validation and maintaining schema


def create_mock_payload():
    with open(os.path.join(current_app.instance_path, 'mock_raw_grid_data.json')) as json_file:
        mock_payload = json.load(json_file)
    return mock_payload

class Grid(Resource):
    """
    Handles all logic for servicing grid data requests and updating grid data model.
    """
    def get(self, region):
        return {"region": region, "data": create_mock_payload()}
        
    # Testing purposes only