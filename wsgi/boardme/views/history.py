from flask import render_template, session, request, jsonify
from sqlalchemy.sql import text

from boardme import app, db

from boardme.models.users import User
from boardme.models.routes import RouteLocation
from boardme.models.history import TravelHistory

@app.route("/my-board", methods=['GET','POST'])
def board_view_and_add(user_id=None):
    if session['user']:
        _user_id = session['user']['id']
        user_travel = TravelHistory.query.filter_by(user_id=_user_id).order_by(TravelHistory.created_ts.desc()).all()
        return render_template('travel-history.html', history=user_travel)
    else :
        return 'Not Logged In', 401


@app.route("/new-board", methods=['POST'])
def board_submit():
    if not session['user']:
        return 'Not logged In', 401
    _user_travel = add_travel_to_db(request)
    return render_template('ticket-confirmation.html',user_travel=_user_travel)


@app.route("/api/travel-history/all", methods=['GET'])
def user_travel_history():
    _user_id = request.args['userId']
    user_travel = TravelHistory.query\
        .filter_by(user_id=_user_id)\
        .order_by(TravelHistory.created_ts.desc())\
        .all()
    result = [travel.to_dict() for travel in user_travel]
    return jsonify(success=True, items=result)


@app.route("/api/travel-history/add", methods=['POST'])
def add_travel_history():
    user_travel = add_travel_to_db(request)
    return jsonify(success=True, item=user_travel)


def add_travel_to_db(request_in):
    if session['user']:
        _user_id = session['user']['id']
    else:
        _user_id = request_in.form['userId']
    _route_start_id = request_in.form['routeStartId']
    _route_end_id = request_in.form['routeEndId']
    return create_travel_record(route_start_id=_route_start_id, route_end_id=_route_end_id, user_id=_user_id)


def create_travel_record(route_start_id, route_end_id, user_id, latitude=None, longitude=None):
    start_route = RouteLocation.query.filter_by(id=route_start_id).first()
    end_route = RouteLocation.query.filter_by(id=route_end_id).first()
    user = User.query.filter_by(id=user_id).first()
    route = start_route.route
    fare_amount = route.route_fare*(end_route.fare_percent - start_route.fare_percent)/100
    user_travel = TravelHistory(user_id=user_id, route_start=route_start_id,
                                route_end=route_end_id, fare_amount=fare_amount)
    if latitude and longitude:
        user_travel.location_lati = latitude
        user_travel.location_longi = longitude
    else:
        user_travel.location_lati = start_route.location_lati
        user_travel.location_longi = start_route.location_longi
    user.wallet -= fare_amount
    db.session.add(user_travel)
    db.session.commit()
    return user_travel


def get_most_recent_boarding_in_route(route_id, stop_order):
    if route_id:
        # get the travel history
        route = db.session.query(RouteLocation)\
            .from_statement(
            text("select rl.* from travel_history th INNER JOIN route_locations rl on th.route_start = rl.id where rl.stop_order < :stop_order and rl.route_id=:route_id  order by th.created_ts DESC, rl.stop_order DESC")).\
            params(stop_order=stop_order, route_id=route_id).first()
        return route
    return None