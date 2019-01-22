""" Register application Blueprints """
import os
from flask import Flask
from instance.config import app_config
from app.dbconnection import DbConnection

from app.api.v2.views.user_view import userV2
from app.api.v2.views.meetups_view import meetupV2
from app.api.v2.views.questions_view import questionV2

from app.api.v1.views.user_view import userV1
from app.api.v1.views.meetups_view import meetupV1
from app.api.v1.views.questions_view import questionV1


def create_app(config_name='development'):
    """ Create flask application object """

    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.register_blueprint(userV1, url_prefix='/api/v1')
    app.register_blueprint(meetupV1, url_prefix='/api/v1')
    app.register_blueprint(questionV1, url_prefix='/api/v1')

    app.register_blueprint(userV2, url_prefix='/api/v2')
    app.register_blueprint(meetupV2, url_prefix='/api/v2')
    app.register_blueprint(questionV2, url_prefix='/api/v2')

    return app
