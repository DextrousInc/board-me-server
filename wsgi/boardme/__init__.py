from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Include config from config.py
app.config.from_pyfile('config.py')

# Create an instance of SQLAclhemy
db = SQLAlchemy(app)


import boardme.views.routes
import boardme.views.users
import boardme.views.history

if __name__ == "__main__":

    db.create_all()
    app.run()
