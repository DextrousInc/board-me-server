from os import environ


#Add your connection string
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/board_me_db'
SQLALCHEMY_ECHO = False
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=transit&traffic_model=optimistic&transit_mode=bus&key={0}&origins={1},{2}&destinations={3},{4}'
GOOGLE_MAPS_API_KEY = 'AIzaSyAAk6I7EB9QfgiUSPZT-MkilxvdPih02ow'
SECRET_KEY = 'L0nd0n6rIdg3i5F@11ingD0wn'
DEBUG = True

#manipulate the environmental configs from OPENSHIFT here
if 'OPENSHIFT_MYSQL_DB_URL' in environ :
    SQLALCHEMY_DATABASE_URI = environ['OPENSHIFT_MYSQL_DB_URL'] + environ['OPENSHIFT_APP_NAME']
