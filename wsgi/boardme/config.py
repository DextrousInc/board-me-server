from os import environ


#Add your connection string
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/board_me_db'
SQLALCHEMY_ECHO = False
SECRET_KEY = 'L0nd0n6rIdg3i5F@11ingD0wn'
DEBUG = True

#manipulate the environmental configs from OPENSHIFT here
if 'OPENSHIFT_MYSQL_DB_URL' in environ :
    SQLALCHEMY_DATABASE_URI = environ['OPENSHIFT_MYSQL_DB_URL'] + environ['OPENSHIFT_APP_NAME']
