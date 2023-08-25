from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    
    if form.validate_on_submit():
        custom_id = form.custom_id.data        

        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('add_link.html', form=form)
        
        if custom_id is None or custom_id == '':
            custom_id = get_unique_short_id()

        url = URLMap(original=form.original_link.data,
                  short=custom_id,)
        db.session.add(url)
        db.session.commit()
        return render_template(
            'add_link.html', form=form, short=custom_id), 200
    return render_template('add_link.html', form=form)

@app.route('/<string:short>', methods=['GET'])
def redirect_url_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
