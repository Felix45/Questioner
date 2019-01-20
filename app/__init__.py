""" Register application Blueprints """
from flask import Flask
from app.api.v2.views.user_view import userV2
from app.api.v2.views.meetups_view import meetupV2
from app.api.v2.views.questions_view import questionV2



def create_app():
    """ Create flask application object """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Okish45@@'
    app.register_blueprint(userV2, url_prefix='/api/v2')
    app.register_blueprint(meetupV2, url_prefix='/api/v2')
    app.register_blueprint(questionV2, url_prefix='/api/v2')

    @app.route("/")
    def function():
        return "hello, World"

    return app
