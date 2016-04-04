from setuptools import setup

setup(name='BoardMeApplication',
      version='1.0',
      description='Server of board me application',
      author='Rajagopal M',
      author_email='rajagopal.a.dinesh.28@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['gevent', 'Flask>=0.7.2', 'MarkupSafe', 'Flask-SQLAlchemy', 'Flask-Migrate', 'MySQL-Python','werkzeug'],
     )
