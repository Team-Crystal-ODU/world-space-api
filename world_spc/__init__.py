# file for app factory and defining routes to resources
import os

from flask import Flask
from flask_restful import Api, Blueprint, Resource, url_for
from flask_pymongo import PyMongo


from world_spc.resources.greeting import HelloWorld

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

    # set up Flask Restful API object
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # Add resources and routing info here. 
    # Resource classes live in resources folder.
    # api.add_resource(Class, '/endpoint0', '/endpoint1')
    api.add_resource(HelloWorld, '/')

    app.register_blueprint(api_bp)

    return app

# sanity check for Pytest basic setup
def hello_world():
    return 'Hello, World!'
