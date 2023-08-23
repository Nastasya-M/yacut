import random
from string import ascii_letters, digits

from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


SHORT_LENGTH = 6


def get_unique_short_id():
    return ''.join(random.choices(list(ascii_letters + digits)), k=6)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if URLMap.query.filter_by(short=custom_id).first():
            flash('Имя {<custom_id} уже занято!')
            return render_template('index.html', form=form)
        if custom_id is None:
            custom_id = get_unique_short_id()
        link = URLMap(original=form.original_link.data,
                  short=custom_id,)
        db.session.add(link)
        db.session.commit()
    return render_template('index.html', form=form)

@app.route('/<string:short>', methods=['GET'])
def redirect_url_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)