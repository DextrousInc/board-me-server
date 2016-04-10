from math import radians


class Coordinate:
    latitude = None
    longitude = None

    def __init__(self, location_lati, location_longi):
        self.longitude = float(location_longi)
        self.latitude = float(location_lati)

    def to_radians(self):
        return Coordinate(location_lati=radians(self.latitude),location_longi = radians(self.longitude))
