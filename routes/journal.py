from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from models import db, DailyJournal
from forms import JournalForm

journal = Blueprint('journal', __name__)

@journal.route("/journal", methods=['GET', 'POST'])
@login_required
def daily_journal():
    from flask import session
    active_account_id = session.get('active_account_id')
    if not active_account_id:
        flash('Please create/select an account first.', 'warning')
        return redirect(url_for('accounts.manage_accounts'))

    form = JournalForm()
    if form.validate_on_submit():
        entry = DailyJournal(date=form.date.data, mood=form.mood.data, 
                             mistakes=form.mistakes.data, lessons=form.lessons.data, 
                             notes=form.notes.data, author=current_user, account_id=active_account_id)
        db.session.add(entry)
        db.session.commit()
        flash('Journal entry saved!', 'success')
        return redirect(url_for('journal.daily_journal'))
    entries = DailyJournal.query.filter_by(user_id=current_user.id, account_id=active_account_id).order_by(DailyJournal.date.desc()).all()
    return render_template('journal.html', form=form, entries=entries)
