# file for app factory and defining routes to resources
import os
import urllib.parse

from flask import Flask, Blueprint
from .extensions import mongo
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
    )
    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('password')
    app.config["MONGO_URI"] = (
            "mongodb://%s:%s@localhost:27017/world-space?authSource=admin"
            % (username, password)
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

    mongo.init_app(app)

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
