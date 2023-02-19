# file for app factory and defining routes to resources
import os

from flask import Flask, Blueprint
from flask_pymongo import PyMongo
from flask_restful import Api

from world_spc.resources.greeting import HelloWorld
from world_spc.resources.grid import Grid
from world_spc.resources.game import Game


# Flask app factory using some boilerplate from docs
# TODO research config, setup options: Database config?
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DB connection depends on Docker container running locally
        MONGO_URI='mongodb://localhost:27017/worldSpace'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # verify instance folder exists (what does this do? check docs)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register MongoDB
    # access db as mongo.db
    mongo = PyMongo(app)
    # register Flask-Restful as blueprint
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # Add resources and routing here
    # Resource classes live in resources folder.
    # api.add_resource(Class, '/endpoint0', '/endpoint1')
    api.add_resource(HelloWorld, '/')
    api.add_resource(Grid, '/grid', endpoint='grid_ep')
    api.add_resource(Game, '/game', endpoint='game_ep')

    app.register_blueprint(api_bp)

    return app
