#!/usr/bin/python3
"""
Starts a Flask web application.

- Defines a route that listens on 0.0.0.0 and port 5000.
- Defines a route for '/states_list' to display a HTML page with the states
  list sorted in alphabetical order.
- Fetchs data from the storage engine.
- Remove the current SQLAlchemy Session after each request.
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list_html():
    """
    Defines a route for /states_list to display a HTML page.
    Fetchs data from the storage engine.
    """
    states = storage.all("State").values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def db_session_teardown(exception):
    """
    Close the storage and remove the current SQLAlchemy Session
    after each request.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
