""" Register application Blueprints """
from flask import Flask 

def create_app():
    """ Create flask application object """
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello, World'

    return app
