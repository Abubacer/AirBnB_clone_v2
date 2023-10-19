#!/usr/bin/python3
"""
Starts a Flask web application.

Defines a route that listens on 0.0.0.0 and port 5000.
Defines a route for the root URL to display 'Hello HBNB!'.
Define a route for '/hbnb' to display 'HBNB'.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Defines a route for the root URL to display 'Hello HBNB!'
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Defines a route for /hbnb to display 'HBNB'
    """
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
