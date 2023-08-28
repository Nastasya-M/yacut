import random
import re
from datetime import datetime

from settings import CUSTOM_ID_LENGTH, PATTERN, SHORT_LENGTH, SYMBOLS
from yacut import db

from .error_handlers import ValidationError

INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
NAME_ALREADY_TAKEN = 'Имя "{custom_id}" уже занято.'
NOT_UNIQUE_NAME = 'Имя {custom_id} уже занято!'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def __get_unique_short_id():
        short_link = ''.join(random.choices(SYMBOLS, k=SHORT_LENGTH))
        if not URLMap.get_short(short_link):
            return short_link

    @staticmethod
    def validate_and_create(original, custom_id=None, validate=False):
        if validate and custom_id or custom_id:
            if len(custom_id) > CUSTOM_ID_LENGTH:
                raise ValidationError(INVALID_NAME)
            if not re.match(PATTERN, custom_id):
                raise ValidationError(INVALID_NAME)
            if URLMap.get_object(custom_id):
                raise ValidationError(
                    NAME_ALREADY_TAKEN.format(custom_id=custom_id)
                    if validate
                    else NOT_UNIQUE_NAME.format(custom_id=custom_id))
        if not custom_id:
            custom_id = URLMap.__get_unique_short_id()
        url = URLMap(original=original, short=custom_id)
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def get_object(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()
