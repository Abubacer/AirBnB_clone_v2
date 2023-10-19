#!/usr/bin/python3
"""
Starts a Flask web application, defines a route that listens on 0.0.0.0
port 5000 and displays 'Hello HBNB!'.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Defines a route that displays 'Hello HBNB!' """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
