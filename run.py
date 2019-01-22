""" run the flask application """
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV'))

if __name__ == "__main__":
    app.run(debug=True)
