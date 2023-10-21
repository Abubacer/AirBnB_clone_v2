#!/usr/bin/python3
"""
Starts a Flask web application.

- Defines a route that listens on 0.0.0.0 and port 5000.
- Defines a route for /states to display a HTML page with:
  + H1 tag: “States”.
  + UL tag: with the list of all State objects.
  + LI tag: description of one State: <state.id>: <B><state.name></B>
  sorted by name in alphabetical order.
- Defines a route for /states/<id> to display a HTML page with:
  If a State object is found with this id
  + H1 tag: “State: ”
  + H3 tag: “Cities:”
  + UL tag: with the list of City objects linked to the State.
  + LI tag: description of one City: <city.id>: <B><city.name></B>
  sorted by name in alphabetical order.
  Otherwise
  + H1 tag: “Not found!”
- Fetchs data from the storage engine.
- Remove the current SQLAlchemy Session after each request.
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_html(id=None):
    """
    Defines a route for /states to display a HTML page.
    Fetchs data from the storage engine.
    """
    state = None
    states = storage.all("State").values()
    for obj in states:
        if obj.id == id:
            state = obj
    return render_template('9-states.html', states=states, id=id, state=state)


@app.teardown_appcontext
def db_session_teardown(exception):
    """
    Close the storage and remove the current SQLAlchemy Session
    after each request.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
