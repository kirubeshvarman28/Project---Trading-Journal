from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from flask_login import login_required, current_user
from models import db, Account
from forms import AccountForm

accounts = Blueprint('accounts', __name__)

@accounts.route("/accounts", methods=['GET', 'POST'])
@login_required
def manage_accounts():
    form = AccountForm()
    if form.validate_on_submit():
        account = Account(name=form.name.data, description=form.description.data, 
                          balance=form.balance.data, owner=current_user)
        db.session.add(account)
        db.session.commit()
        session['active_account_id'] = account.id
        flash(f'Account "{account.name}" created and set as active!', 'success')
        return redirect(url_for('main.dashboard'))
    
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template('accounts.html', form=form, accounts=user_accounts)

@accounts.route("/accounts/select/<int:account_id>")
@login_required
def select_account(account_id):
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('accounts.manage_accounts'))
    
    session['active_account_id'] = account.id
    flash(f'Switched to account: {account.name}', 'success')
    return redirect(request.referrer or url_for('main.dashboard'))

@accounts.route("/accounts/edit/<int:account_id>", methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('accounts.manage_accounts'))
    
    form = AccountForm()
    if form.validate_on_submit():
        account.name = form.name.data
        account.description = form.description.data
        account.balance = form.balance.data
        db.session.commit()
        flash(f'Account "{account.name}" updated!', 'success')
        return redirect(url_for('accounts.manage_accounts'))
    elif request.method == 'GET':
        form.name.data = account.name
        form.description.data = account.description
        form.balance.data = account.balance
    
    return render_template('accounts.html', form=form, accounts=Account.query.filter_by(user_id=current_user.id).all(), edit_mode=True, edit_account=account)

@accounts.route("/accounts/delete/<int:account_id>", methods=['POST'])
@login_required
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('accounts.manage_accounts'))
    
    # Prevent deleting the last account
    total_accounts = Account.query.filter_by(user_id=current_user.id).count()
    if total_accounts <= 1:
        flash('You must have at least one account.', 'warning')
        return redirect(url_for('accounts.manage_accounts'))
    
    # If active account is being deleted, switch to another one
    if session.get('active_account_id') == account.id:
        other_account = Account.query.filter(Account.user_id == current_user.id, Account.id != account.id).first()
        session['active_account_id'] = other_account.id
    
    db.session.delete(account)
    db.session.commit()
    flash(f'Account "{account.name}" and all associated data deleted.', 'success')
    return redirect(url_for('accounts.manage_accounts'))
