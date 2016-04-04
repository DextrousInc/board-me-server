from flask import render_template

from boardme import app, db


@app.route("/")
def home():
    return render_template('home.html', logged_in=False)
