from flask_restful import Resource

from flask import request, abort
from marshmallow import Schema, fields


class HardwareUpdateSchema(Schema):
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)


u_schema = HardwareUpdateSchema()


class Hardware(Resource):

    def post(self):
        errors = u_schema.validate()
        if errors:
            abort(400, str(errors))

        start = request.args['start']
        end = request.args['end']
