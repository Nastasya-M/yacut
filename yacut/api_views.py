from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage, ValidationError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_short_link():

    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    try:
        url = URLMap.validate_and_create(
            data.get('url'), data.get('custom_id'), True
        )
        return jsonify({
            'url': data['url'],
            'short_link': url_for(
                'redirect_url_view',
                short=url.short,
                _external=True,
            )}), HTTPStatus.CREATED
    except ValidationError as error:
        raise InvalidAPIUsage(message=error.message)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    url = URLMap.get_object(short_id)
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
