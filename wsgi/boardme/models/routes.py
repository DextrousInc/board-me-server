from sqlalchemy.orm import relationship
from boardme import db
import datetime


class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(128))
    route_start = db.Column(db.String(128))
    route_end = db.Column(db.String(128))
    beacon_id = db.Column(db.String(128))
    route_fare = db.Column(db.Float)
    created_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    last_updated_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    stops = relationship('RouteLocation', back_populates='route')

    def __init__(self, route_name, route_start, route_end, beacon_id, route_fare):
        self.route_name = route_name
        self.route_start = route_start
        self.route_end = route_end
        self.beacon_id = beacon_id
        self.route_fare = route_fare

    def to_dict(self):
        return {
            'id' : self.id,
            'routeName': self.route_name,
            'routeStart': self.route_start,
            'routeEnd': self.route_end,
            'beaconId': self.beacon_id,
            'routeFare': self.route_fare,
            'createdTS': self.created_ts,
            'lastUpdateTS': self.last_updated_ts
        }


class RouteLocation(db.Model):
    __tablename__ = 'route_locations'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    stop_name = db.Column(db.String(128))
    stop_order = db.Column(db.Integer)
    fare_percent = db.Column(db.Float)
    location_lati = db.Column(db.Float)
    location_longi = db.Column(db.Float)
    created_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    last_updated_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    route = relationship('Route', back_populates='stops')

    def __init__(self, route_id, stop_name, stop_order, fare_percent, location_lati, location_longi):
        self.route_id = route_id
        self.stop_name = stop_name
        self.stop_order = stop_order
        self.fare_percent = fare_percent
        self.location_lati = location_lati
        self.location_longi = location_longi

    def to_dict(self):
        return {
            'id' : self.id,
            'routeId' : self.route_id,
            'stopName' : self.stop_name,
            'stopOrder' : self.stop_order,
            'farePercent' : self.fare_percent,
            'locationLatitute' : self.location_lati,
            'locationLongitute' : self.location_longi,
            'createdTS' : self.created_ts,
            'lastUpdateTS' : self.last_updated_ts
        }
