from flask_restful import Resource

from world_spc.extensions import mongo


class HelloWorld(Resource):
    def get(self):
        mongo.db.hello.insert_one({"some": "very", "random": "document"})
