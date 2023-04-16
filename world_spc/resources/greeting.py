from flask_restful import Resource
from flask import request
import json
import requests
import sys


from world_spc.extensions import mongo
from world_spc.scribes.grid_scribe import update_grid_data, parse_latest
from world_spc.mocking.hw_mocker import generate


class HelloWorld(Resource):
    def get(self):
        # return update_grid_data(mongo.db)
        payload = {"key1": 1, "key2": 2}
        r = requests.post('http://localhost:4005/', json=payload)
        return r.json()

    def post(self):
        generate(mongo.db)
        return "Generated mock hw data for ecogamer."
