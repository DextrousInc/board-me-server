from math import cos, sin, asin, sqrt
from flask import render_template, request, json, jsonify

import requests
from boardme import app, db
from boardme.models.coordinates import Coordinate
from boardme.models.routes import Route, RouteLocation
from boardme.views.history import get_most_recent_boarding_in_route


@app.route("/routes")
def view_routes():
    routes = Route.query.all()
    return render_template('routes.html', routes=routes)


@app.route("/board-me", methods=['GET', 'POST'])
def board_routes():
    route_id = None
    start_route = None
    end_route = None
    if request.method == 'POST':
        route_id = request.form.get('routeId', None)
        start_route = request.form.get('startRoute', None)
        end_route = request.form.get('endRoute', None)
    _selected_route = None
    _all_routes = None
    _selected_start_point = None
    _all_stops = None
    _selected_end_point = None
    if route_id:
        _selected_route = Route.query.filter_by(id=route_id).first()
        if start_route:
            _selected_start_point = RouteLocation.query.filter_by(id=start_route).first()
            if end_route:
                _selected_end_point = RouteLocation.query.filter_by(id=end_route).first()
            else:
                _all_stops = RouteLocation \
                    .query \
                    .filter(RouteLocation.stop_order > _selected_start_point.stop_order) \
                    .filter_by(route_id=route_id)\
                    .order_by(RouteLocation.stop_order.asc())\
                    .all()
        else:
            _all_stops = RouteLocation.query.filter_by(route_id=route_id)\
                .order_by(RouteLocation.stop_order.asc())\
                .all()
    else:
        _all_routes = Route.query.all()

    return render_template('board.html', all_routes=_all_routes,
                           selected_route=_selected_route, all_stops=_all_stops,
                           selected_start_point=_selected_start_point,
                           selected_end_point=_selected_end_point)


@app.route("/route-locations/<route_id>")
def view_route_locations(route_id=None):
    route_locations = RouteLocation.query.filter_by(route_id=route_id).order_by(RouteLocation.stop_order.asc()).all()
    return render_template('route-locations.html', route_locations=route_locations)


@app.route("/board-wait", methods=['GET', 'POST'])
def board_wait():
    route_id = None
    start_route = None

    _all_routes = None
    _selected_route = None
    _all_stops = None
    _selected_stop = None
    _estimated_time = None
    if request.method == 'POST':
        route_id = request.form.get('routeId', None)
        start_route = request.form.get('startRoute', None)

    if route_id:
        _selected_route = Route.query.filter_by(id=route_id).first()
        if start_route:
            _selected_stop = RouteLocation.query.filter_by(id=start_route).first()

            # get the most recent boarding location from the travel history
            recent_boarding_location = get_most_recent_boarding_in_route(route_id=route_id, stop_order=_selected_stop.stop_order)
            # print recent_boarding_location.to_dict()
            if _selected_stop and recent_boarding_location:
                # get the ETA
                _estimated_time = calculate_min_wait_time(from_location=_selected_stop, to_location=recent_boarding_location)
                # print _estimated_time
        else:
            _all_stops = RouteLocation.query.filter_by(route_id=route_id)\
                .order_by(RouteLocation.stop_order.asc())\
                .all()
    else:
        _all_routes = Route.query.all()

    return render_template('board-wait.html', all_routes=_all_routes, selected_route=_selected_route,
                           all_stops=_all_stops, selected_stop=_selected_stop, estimated_time=_estimated_time)


@app.route("/api/routes/all")
def get_routes():
    routes = Route.query.all()
    all_routes = [route.to_dict() for route in routes]
    return jsonify(success=True, items=all_routes)


@app.route("/api/routes/locations/all", methods=["GET"])
def get_route_locations():
    _route_id = request.args['routeId']
    route_locations = RouteLocation.query.filter_by(route_id=_route_id)\
        .order_by(RouteLocation.stop_order.asc())\
        .all()
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
                  route_end=_route_end, route_fare=_route_fare, beacon_id=_beacon_id)
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


@app.route("/api/board-wait", methods=['GET'])
def api_board_wait():
    latitude = request.args['latitude']
    longitude = request.args['longitude']
    route_id = request.args['routeId']

    # get the nearest stop of the user in the given route
    route_locations = RouteLocation.query.filter_by(route_id=route_id)\
        .order_by(RouteLocation.stop_order.asc())\
        .all()
    user_location = Coordinate(location_lati=latitude, location_longi=longitude)
    close_stop = get_the_closest_location(location=user_location, route_locations=route_locations)

    # get the most recent boarding location from the travel history
    recent_boarding_location = get_most_recent_boarding_in_route(route_id=route_id, stop_order=close_stop.stop_order)
    # print recent_boarding_location.to_dict()
    if close_stop and recent_boarding_location:
        # get the ETA
        _eta_data = calculate_min_wait_time(from_location=close_stop, to_location=recent_boarding_location)
        return jsonify(success=True, item={'eta': _eta_data, 'closeStop': close_stop.to_dict()})
    return "Invalid input", 403


@app.route("/api/board-me", methods=['GET'])
def api_board_me():
    latitude = request.args['latitude']
    longitude = request.args['longitude']
    _beacon_id = request.args['beaconId']
    user_id = request.args['userId']

    # get the corresponding route of the beacon
    current_route = Route.query.filter_by(beacon_id=_beacon_id).first()

    # get the nearest stop of the user in the given route
    route_locations = RouteLocation.query\
        .filter_by(route_id=current_route.id)\
        .order_by(RouteLocation.stop_order.asc())\
        .all()
    user_location = Coordinate(location_lati=latitude, location_longi=longitude)
    close_stop = get_the_closest_location(location=user_location, route_locations=route_locations)

    # get all route locations after the close stop
    all_stops = RouteLocation.query\
        .filter(RouteLocation.stop_order > close_stop.stop_order) \
        .filter_by(route_id=current_route.id)\
        .order_by(RouteLocation.stop_order.asc())\
        .all()

    if close_stop and current_route and len(all_stops) > 0:
        # get the selected route and stops
        next_stops = [stop.to_dict() for stop in all_stops]
        return jsonify(selectedRoute=current_route.to_dict(), selectedStop=close_stop.to_dict(), nextStops=next_stops)
    return "Invalid input", 403


def get_the_closest_location(location, route_locations):
    # loop through the route_locations and find the nearest one
    picked_location = None
    if len(route_locations) > 0:
        picked_location = route_locations[0]
        picked_coords = Coordinate(picked_location.location_lati, picked_location.location_longi)
        picked_distance = calculate_distance_between(from_location=location, to_location=picked_coords)
        for stop_location in route_locations:
            this_coords = Coordinate(stop_location.location_lati, stop_location.location_longi)
            this_distance = calculate_distance_between(from_location=location, to_location=this_coords)
            if this_distance < picked_distance:
                picked_location = stop_location
    return picked_location


def calculate_distance_between(from_location, to_location):
    from_location = from_location.to_radians()
    to_location = to_location.to_radians()
    # haversine formula
    longitude_difference = from_location.longitude - to_location.longitude
    latitude_difference = from_location.latitude - to_location.latitude

    a = sin(latitude_difference / 2) ** 2 + cos(from_location.latitude) * cos(to_location.latitude) * sin(
        longitude_difference / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance_in_km = 6367 * c
    return distance_in_km


def calculate_min_wait_time(from_location, to_location):
    api_key = app.config['GOOGLE_MAPS_API_KEY']
    api_url = app.config['GOOGLE_MAPS_API_URL']
    if api_key and api_url:
        # calculate the ETA with google directions api
        url = api_url.format(api_key, from_location.location_lati, from_location.location_longi, to_location.location_lati,
                             to_location.location_longi)
        api_response = requests.get(url).json()
        # print api_response
        '''
            RESPONSE FORMAT
            {
               "destination_addresses" : [ "334-350 Hicks St, Brooklyn, NY 11201, USA" ],
               "origin_addresses" : [ "565-569 Vermont St, Brooklyn, NY 11207, USA" ],
               "rows" : [
                  {
                     "elements" : [
                        {
                           "distance" : {
                              "text" : "10.4 km",
                              "value" : 10411
                           },
                           "duration" : {
                              "text" : "32 mins",
                              "value" : 1947
                           },
                           "status" : "OK"
                        }
                     ]
                  }
               ],
               "status" : "OK"
            }
        '''
        # this will always have one item in tha array of rows
        from_location_name = api_response["origin_addresses"][0]
        to_location_name = api_response["destination_addresses"][0]
        duration = api_response["rows"][0]["elements"][0]["duration"]["text"]  # in seconds
        distance = api_response["rows"][0]["elements"][0]["distance"]["text"]  # in metres
        return {'from_location':from_location_name, 'to_location':to_location_name, 'duration':duration, 'distance':distance}
