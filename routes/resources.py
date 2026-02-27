from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from models import db, Resource
from forms import ResourceForm

resources = Blueprint('resources', __name__)

@resources.route("/academy", methods=['GET', 'POST'])
@login_required
def resource_center():
    form = ResourceForm()
    if form.validate_on_submit():
        res = Resource(title=form.title.data, link=form.link.data, 
                        category=form.category.data, author=current_user)
        db.session.add(res)
        db.session.commit()
        flash('Resource added!', 'success')
        return redirect(url_for('resources.resource_center'))
    all_res = Resource.query.filter_by(user_id=current_user.id).all()
    return render_template('resources.html', form=form, resources=all_res)
