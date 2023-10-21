#!/usr/bin/python3
"""
Starts a Flask web application.

- Defines a route that listens on 0.0.0.0 and port 5000.
- Defines a route for /cities_by_states to display a HTML page with:
  + H1 tag: “States”.
  + UL tag: with the list of all State.
  + LI tag: description of one State: <state.id>: <B><state.name></B>
  + UL tag: with the list of City objects linked to the State.
  + LI tag: description of one City: <city.id>: <B><city.name></B>
  sorted by name in alphabetical order.
- Fetchs data from the storage engine.
- Remove the current SQLAlchemy Session after each request.
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_states_html():
    """
    Defines a route for /cities_by_states to display a HTML page.
    Fetchs data from the storage engine.
    """
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def db_session_teardown(exception):
    """
    Close the storage and remove the current SQLAlchemy Session
    after each request.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
