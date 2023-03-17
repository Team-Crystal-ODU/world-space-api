from flask_restful import Resource
from flask import request

from world_spc.extensions import mongo


class HelloWorld(Resource):
    def get(self):
        data = mongo.db.hello.find_one({"hello": "world"})
        # _id in BSON does not convert to JSON
        # stripping from output since it's not useful to API users
        data.pop('_id')
        return data

    def post(self):
        msg = request.form
        mongo.db.hello.insert_one({"message": msg['Message']})
        return 'Message received!'
