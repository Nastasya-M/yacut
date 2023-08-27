import os
from string import ascii_letters, digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')


PATTERN = r'^[a-zA-Z0-9]{1,16}$'
SYMBOLS = ascii_letters + digits
SHORT_LENGTH = 6
