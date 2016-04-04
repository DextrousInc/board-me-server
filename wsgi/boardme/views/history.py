from flask import render_template, request, jsonify

from boardme import app, db

from boardme.models.users import User
from boardme.models.routes import RouteLocation
from boardme.models.history import TravelHistory


@app.route("/board/<user_id>", methods=['GET','POST'])
def board_view_and_add(user_id=None):
    if request.method == 'POST':
        user_travel = add_travel_to_db(request)
        return render_template('new-travel.html', success=True, item=user_travel)
    else:
        user_travel = TravelHistory.query.filter_by(user_id=user_id).all()
        return render_template('travel-history.html', history=user_travel)


@app.route("/new-board/<user_id>", methods=['GET'])
def board_view(user_id):
    return render_template('new-travel.html', user_id=user_id)


@app.route("/api/travel-history/all", methods=['GET'])
def user_travel_history():
    _user_id = request.args['userId']
    user_travel = TravelHistory.query.filter_by(user_id=_user_id).all()
    result = [travel.to_dict() for travel in user_travel]
    return jsonify(success=True, items=result)


@app.route("/api/travel-history/add", methods=['POST'])
def add_travel_history():
    user_travel = add_travel_to_db(request)
    return jsonify(success=True, item=user_travel.to_dict())


def add_travel_to_db(request_in):
    _user_id = request_in.form['userId']
    _route_start_id = request_in.form['routeStartId']
    _route_end_id = request_in.form['routeEndId']
    start_route = RouteLocation.query.filter_by(id=_route_start_id).first()
    end_route = RouteLocation.query.filter_by(id=_route_end_id).first()
    user = User.query.filter_by(id=_user_id).first()
    route = start_route.route
    fare_amount = route.route_fare*(end_route.fare_percent - start_route.fare_percent)/100
    user_travel = TravelHistory(user_id=_user_id, route_start=_route_start_id,
                                route_end=_route_end_id, fare_amount=fare_amount)
    user.wallet -= fare_amount
    db.session.add(user_travel)
    db.session.commit()
    return user_travel
