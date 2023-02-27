from flask_restful import Resource
from flask import request, abort
from marshmallow import Schema, fields


class CarbonQuerySchema(Schema):
    user = fields.Str(required=True)


q_schema = CarbonQuerySchema()


class Carbon(Resource):
    def get(self):
        errors = q_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        return
