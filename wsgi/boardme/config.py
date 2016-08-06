from os import environ

# Add your connection string
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/board_me_db'
SQLALCHEMY_ECHO = False
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=transit&traffic_model=optimistic&transit_mode=bus&key={0}&origins={1},{2}&destinations={3},{4}'
GOOGLE_MAPS_API_KEY = 'AIzaSyAAk6I7EB9QfgiUSPZT-MkilxvdPih02ow'
SECRET_KEY = 'L0nd0n6rIdg3i5F@11ingD0wn'
OLD_TWILIO_ACCOUNT_SID = 'AC3adfa6836a1a8fa5fb01e9f5f5fb7d89'
OLD_TWILIO_AUTH_TOKEN = '249aaac3f241ff91857dd8385076c4fe'
OLD_TWILIO_SENDER_NUMBER = '+15005550006'
TWILIO_ACCOUNT_SID = 'AC720777d56808a21bd0d71cc6cf7b3090'
TWILIO_AUTH_TOKEN = '3ad4318dcfadda199bd627221379475e'
TWILIO_SENDER_NUMBER = '+17653990361'
NEXMO_API_KEY = 'f9f3884c'
NEXMO_API_SECRET = 'eb2184b89183fd15'
DEBUG = True

# manipulate the environmental configs from OPENSHIFT here
if 'OPENSHIFT_MYSQL_DB_URL' in environ:
    SQLALCHEMY_DATABASE_URI = environ['OPENSHIFT_MYSQL_DB_URL'] + environ['OPENSHIFT_APP_NAME']
