from flask_restful import Resource
from flask import request

from world_spc.extensions import mongo
from world_spc.scribes.grid_scribe import update_grid_data


class HelloWorld(Resource):
    def get(self):
        return update_grid_data(mongo.db)

    def post(self):
        msg = request.form
        mongo.db.hello.insert_one({"message": msg['Message']})
        return 'Message received!'
