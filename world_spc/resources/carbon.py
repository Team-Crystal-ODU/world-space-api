from flask_restful import Resource
from flask import request, abort
from marshmallow import Schema, fields
from world_spc.common import util


class CarbonQuerySchema(Schema):
    user = fields.Str(required=True)


q_schema = CarbonQuerySchema()


class Carbon(Resource):
    def get(self):
        errors = q_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        if request.args['user'] != 'ecogamer':
            abort(400, 'Could not find user.')
        return util.create_mock_carbon_readout()
