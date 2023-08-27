from flask import flash, redirect, render_template, url_for

from . import app
from .error_handlers import ValidationError
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if not form.validate_on_submit():
        return render_template('add_link.html', form=form)
    try:
        url = URLMap.validate_and_create(
            form.original_link.data,
            form.custom_id.data)
        return render_template(
            'add_link.html',
            form=form,
            short_link=url_for(
                'redirect_url_view',
                short=url.short,
                _external=True,
            ))
    except ValidationError as error:
        flash(error.message)
        return render_template('add_link.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url_view(short):
    return redirect(URLMap.get_or_404(short).original)
