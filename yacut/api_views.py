import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    PATTERN = r'^[a-zA-Z0-9]{1,16}$'

    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    short_id = data.get('custom_id')
    if short_id:
        if len(short_id) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if not re.match(PATTERN, short_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    if short_id is None or short_id == '':
        data['custom_id'] = get_unique_short_id()
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
