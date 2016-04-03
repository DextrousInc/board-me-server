from flask import render_template, request, jsonify

from wsgi import app, db

from wsgi.models.users import User


@app.route("/users")
def view_users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


@app.route("/api/users/all")
def get_users():
    all_users = User.query.all()
    result = [user.to_dict() for user in all_users]
    return jsonify(items=result, success=True)


@app.route("/api/users/add", methods=['POST'])
def add_user():
    _first_name = request.form['firstName']
    _last_name = request.form['lastName']
    _username = request.form['username']
    _password = request.form['password']
    _email = request.form['email']
    _wallet = 10000
    _currency_type = 'INR'
    new_user = User(first_name=_first_name, last_name=_last_name,
                    username=_username, password=_password,email=_email, wallet=_wallet,currency_type=_currency_type)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(success=True, result= new_user.to_dict())