#!/usr/bin/python3
"""
Starts a Flask web application.

- Defines a route that listens on 0.0.0.0 and port 5000.
- Defines a route for the root URL to display 'Hello HBNB!'.
- Defines a route for '/hbnb' to display 'HBNB'.
- Defines a route for '/c/<text>' to display 'C' followed by the value
of the text variable.
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


@app.route('/c/<text>', strict_slashes=False)
def show_text_value(text):
    """
    Defines a route for /c/ to display 'C' followed by the value of
    the text variable.
    """
    text = text.replace('_', ' ')
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
