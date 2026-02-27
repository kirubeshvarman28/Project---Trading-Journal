from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from models import db, Playbook
from forms import PlaybookForm
import os
from werkzeug.utils import secure_filename

playbooks = Blueprint('playbooks', __name__)

@playbooks.route("/playbooks", methods=['GET', 'POST'])
@login_required
def playbook_list():
    from flask import session
    active_account_id = session.get('active_account_id')
    if not active_account_id:
        flash('Please create/select an account first.', 'warning')
        return redirect(url_for('accounts.manage_accounts'))

    form = PlaybookForm()
    if form.validate_on_submit():
        filename = None
        if form.screenshot.data:
            filename = secure_filename(form.screenshot.data.filename)
            form.screenshot.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        playbook = Playbook(name=form.name.data, rules=form.rules.data, 
                             risk_pct=form.risk_pct.data, screenshot=filename, 
                             author=current_user, account_id=active_account_id)
        db.session.add(playbook)
        db.session.commit()
        flash('Playbook added!', 'success')
        return redirect(url_for('playbooks.playbook_list'))
    setups = Playbook.query.filter_by(user_id=current_user.id, account_id=active_account_id).all()
    return render_template('playbooks.html', form=form, playbooks=setups)
