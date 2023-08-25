from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = URLField(
        'Добавьте свою короткую ссылку',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
