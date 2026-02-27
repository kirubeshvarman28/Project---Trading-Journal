from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from models import db, Note
from forms import NoteForm

notebook = Blueprint('notebook', __name__)

@notebook.route("/notes", methods=['GET', 'POST'])
@login_required
def notes():
    from flask import session
    active_account_id = session.get('active_account_id')
    if not active_account_id:
        flash('Please create/select an account first.', 'warning')
        return redirect(url_for('accounts.manage_accounts'))

    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user, account_id=active_account_id)
        db.session.add(note)
        db.session.commit()
        flash('Note created!', 'success')
        return redirect(url_for('notebook.notes'))
    all_notes = Note.query.filter_by(user_id=current_user.id, account_id=active_account_id).order_by(Note.created_at.desc()).all()
    return render_template('notebook.html', form=form, notes=all_notes)
