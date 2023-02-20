from flask_restful import Resource
from flask import request, abort, current_app
from marshmallow import Schema, fields
from world_spc.common import util


class GameQuerySchema(Schema):
    userID = fields.Int(required=True)


q_schema = GameQuerySchema()


class Game(Resource):
    def get(self):
        errors = q_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        # TODO Refactor authentication to an auth.py
        if request.args["userID"] != '12345':
            abort(400, 'Could not locate user')

        return util.create_mock_game_state()
