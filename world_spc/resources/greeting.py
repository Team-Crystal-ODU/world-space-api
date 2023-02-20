from flask_restful import Resource

from world_spc.extensions import mongo


class HelloWorld(Resource):
    def get(self):
        data = mongo.db.hello.find_one({"some": "very"})
        data.pop('_id')
        return data
