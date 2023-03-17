from flask_restful import Resource

from flask import request, abort
from marshmallow import Schema, fields

from world_spc.extensions import mongo
from world_spc.mocking import hw_mocker


class HardwareUpdateSchema(Schema):
    user = fields.Str(required=True)


u_schema = HardwareUpdateSchema()


class Hardware(Resource):

    def post(self):
        errors = u_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        # TODO Check if user is in a list of users
        # Possibly user a simple decorator for this
        if request.args['user'] == 'ecogamer':
            hw_mocker.generate(mongo.db)
        return 'Write succeeded.'
