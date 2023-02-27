from flask_restful import Resource

# from world_spc.extensions import mongo


class HelloWorld(Resource):
    def get(self):
        # data = mongo.db.hello.find_one({"some": "very"})
        # _id in BSON does not convert to JSON
        # stripping from output since it's not useful to API users
        # data.pop('_id')
        return {'Hello': 'From World Space!'}
