""" Register application Blueprints """
from flask import Flask
from app.api.v1.views.user_view import userV1
from app.api.v1.views.meetups_view import meetupV1
from app.api.v1.views.questions_view import questionV1


def create_app():
    """ Create flask application object """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Okish45@@'
    app.register_blueprint(userV1, url_prefix='/api/v1')
    app.register_blueprint(meetupV1, url_prefix='/api/v1')
    app.register_blueprint(questionV1, url_prefix='/api/v1')

    @app.route("/")
    def function():
        return "hello, World"

    return app
