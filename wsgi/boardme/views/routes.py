from flask import render_template, request, jsonify

from boardme import app, db

from boardme.models.routes import Route, RouteLocation


@app.route("/routes")
def view_routes():
    routes = Route.query.all()
    return render_template('routes.html', routes=routes)


@app.route("/route-locations/<route_id>")
def view_route_locations(route_id=None):
    route_locations = RouteLocation.query.filter_by(route_id=route_id)
    return render_template('route-locations.html', route_locations=route_locations)


@app.route("/api/routes/all")
def get_routes():
    routes = Route.query.all()
    all_routes = [route.to_dict() for route in routes]
    return jsonify(success=True, items=all_routes)


@app.route("/api/routes/locations/all", methods=["GET"])
def get_route_locations():
    _route_id = request.args['routeId']
    route_locations = RouteLocation.query.filter_by(route_id=_route_id).all()
    all_route_locations = [route_loc.to_dict() for route_loc in route_locations]
    return jsonify(success=True, items=all_route_locations)


@app.route("/api/routes/add", methods=['POST'])
def add_route():
    _route_name = request.form['routeName']
    _route_start = request.form['routeStart']
    _route_end = request.form['routeEnd']
    _beacon_id = request.form['beaconId']
    _route_fare = request.form['routeFare']
    route = Route(route_name=_route_name, route_start=_route_start,
                  route_end=_route_end,route_fare=_route_fare, beacon_id=_beacon_id)
    db.session.add(route)
    db.session.commit()
    return jsonify(success=True, item=route.to_dict())


@app.route("/api/routes/locations/add", methods=['POST'])
def add_route_location():
    _route_id = request.form['routeId']
    _stop_name = request.form['stopName']
    _stop_order = request.form['stopOrder']
    _fare_percent = request.form['farePercent']
    _latitude = request.form['latitude']
    _longitude = request.form['longitude']
    route_location = RouteLocation(route_id=_route_id, stop_name=_stop_name,
                          stop_order=_stop_order, fare_percent=_fare_percent,
                          location_lati=_latitude, location_longi=_longitude)
    db.session.add(route_location)
    db.session.commit()
    return jsonify(success=True, item=route_location.to_dict())
