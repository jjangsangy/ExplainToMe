import pprint

from flask_debugtoolbar import DebugToolbarExtension
from flask_script import Manager

from ExplainToMe import app

app.debug = True


manager = Manager(app)
toolbar = DebugToolbarExtension(app)

if __name__ == "__main__":
    manager.run()
