from flask_restful import Resource
from flask import request, abort
from marshmallow import Schema, fields
from world_spc.scribes import carbon_scribe
from world_spc.extensions import mongo


class CarbonQuerySchema(Schema):
    user = fields.Str(required=True)


q_schema = CarbonQuerySchema()


class Carbon(Resource):
    def get(self):
        errors = q_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        user = request.args['user']
        # TODO run a check against collection of usernames
        if user != 'ecogamer':
            abort(400, 'Could not find user.')
        return carbon_scribe.get_carbon_readout(user, mongo.db)
