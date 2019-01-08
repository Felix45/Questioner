""" Adds a flask application """
from flask import Flask , request , jsonify

app = Flask(__name__)

@app.route("/")
def get():
    return "hello, World"

if __name__ == "__main__":
    app.run(debug=True)






