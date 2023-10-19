#!/usr/bin/python3
"""
Starts a Flask web application.

- Defines a route that listens on 0.0.0.0 and port 5000.
- Defines a route for the root URL to display 'Hello HBNB!'.
- Defines a route for '/hbnb' to display "HBNB".
- Defines a route for '/c/<text>' to display 'C' followed by the value
of the text variable.

- Defines a route for '/python/<text>' to display 'Python', followed by
the value of the text variable.
- Sets the default value of text to 'is cool'.

- Defines a route for '/number/<n>' to display 'n is a number'.
- Only if 'n' is an integer.
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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def show_python(text):
    """
    Defines a route for /python/ to display 'Python' followed by the
    value of the text var. Sets the default value of text to 'is cool'
    """
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    Defines a route for /number/ to display 'n is a number'
    only if 'n' is an integer
    """
    n = str(n)
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
