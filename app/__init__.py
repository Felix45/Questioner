""" Register application Blueprints """
from flask import Flask
from app.api.v2.views.user_view import userV2
#from app.api.v1.views.meetups_view import meetupV1


def create_app():
    """ Create flask application object """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Okish45@@'
    app.register_blueprint(userV2, url_prefix='/api/v2')
    #app.register_blueprint(meetupV1, url_prefix='/api/v1')

    @app.route("/")
    def function():
        return "hello, World"

    return app
