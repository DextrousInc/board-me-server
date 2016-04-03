from flask import render_template

from wsgi import app, db


@app.route("/")
def home():
    return render_template('home.html', logged_in=False)
