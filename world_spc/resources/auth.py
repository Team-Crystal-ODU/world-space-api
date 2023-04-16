from flask_restful import Resource
from flask import request, abort
from marshmallow import Schema, fields
from world_spc.extensions import mongo


class Auth(Resource):
    def get(self):
        pass

    def post(self):
        pass
