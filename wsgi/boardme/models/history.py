from boardme import db
from sqlalchemy.orm import relationship
import datetime

from boardme.models.routes import RouteLocation


class TravelHistory(db.Model):
    __tablename__ = 'travel_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    route_start = db.Column(db.Integer, db.ForeignKey('route_locations.id'))
    route_end = db.Column(db.Integer, db.ForeignKey('route_locations.id'))
    fare_amount = db.Column(db.Float)
    location_lati = db.Column(db.Float(15, 3))
    location_longi = db.Column(db.Float(15, 3))
    created_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    last_updated_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    user = relationship('User', back_populates='history')
    start_route = relationship(RouteLocation, primaryjoin=route_start == RouteLocation.id)
    end_route = relationship(RouteLocation, primaryjoin=route_end == RouteLocation.id)

    def __init__(self, user_id, route_start, route_end, fare_amount):
        self.user_id = user_id
        self.route_start = route_start
        self.route_end = route_end
        self.fare_amount = fare_amount

    def to_dict(self):
        return {
            'userId': self.user_id,
            'id': self.id,
            'routeStartId': self.route_start,
            'routeEndId': self.route_end,
            'fareAmount': self.fare_amount,
            'latitude': float(self.location_lati),
            'longitude': float(self.location_longi),
            'startRoute': self.start_route.to_dict(),
            'endRoute': self.end_route.to_dict(),
            'user': self.user.to_dict(),
            'createdTS': self.created_ts,
            'lastUpdatedTS': self.last_updated_ts
        }
