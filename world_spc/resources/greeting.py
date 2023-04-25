from flask_restful import Resource
from flask import request
import requests
from datetime import datetime


from world_spc.extensions import mongo
from world_spc.mocking.hw_mocker import generate


class HelloWorld(Resource):
    def get(self):
        # return update_grid_data(mongo.db)
        payload = {"key1": 1, "key2": 2}
        r = requests.post('http://localhost:4005/', json=payload)
        return r.json()

    def post(self):
        start = datetime.strptime(request.args['start'], '%Y-%m-%dT%H:%M:%S')
        end = datetime.strptime(request.args['end'], '%Y-%m-%dT%H:%M:%S')
        generate(start, end, mongo.db)
        return "Generated mock hw data for ecogamer."
