from flask_restful import Resource
from flask import request, abort
from marshmallow import Schema, fields
from world_spc.extensions import mongo


class AuthSchema(Schema):
    user = fields.Str(required=True)
    password = fields.Str(required=True)


def check_user_and_password(db, user, password):
    col = db['auth']
    if col.count_documents({"user": user}) > 0:
        id = col.find_one({"user": user})["_id"]
        if col.find_one({"_id": id})['password'] == password:
            return True
        else:
            return False
    else:
        return False


schema = AuthSchema()


class Auth(Resource):
    def get(self):
        errors = schema.validate(request.form)
        if errors:
            abort(400, str(errors))

        user = request.form['user']
        password = request.form['password']

        if check_user_and_password(mongo.db, user, password):
            return "Success."
        else:
            abort(400, "User and password combination not found.")

    def post(self):
        errors = schema.validate(request.form)
        if errors:
            abort(400, str(errors))

        user = request.form['user']
        password = request.form['password']

        col = mongo.db['auth']
        col.insert_one({'user': user, 'password': password})

        return f"User {user} successfully registered."
