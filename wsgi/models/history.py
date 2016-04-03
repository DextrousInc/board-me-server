from wsgi import db
import datetime


class TravelHistory(db.Model):
    __tablename__ = 'travel_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    route_start = db.Column(db.Integer, db.ForeignKey('route_locations.id'))
    route_end = db.Column(db.Integer, db.ForeignKey('route_locations.id'))
    fare_amount = db.Column(db.Float)
    created_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    last_updated_ts = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, user_id, route_start, route_end, fare_amount):
        self.user_id = user_id
        self.route_start = route_start
        self.route_end = route_end
        self.fare_amount = fare_amount

    def to_dict(self):
        return {
            'userId': self.user_id,
            'routeStart': self.route_start,
            'routeEnd': self.route_end,
            'fareAmount': self.fare_amount,
            'createdTS': self.created_ts,
            'lastUpdatedTS': self.last_updated_ts
        }
