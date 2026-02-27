from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, abort
from flask_login import login_required, current_user
from models import db, Trade
from forms import TradeForm
import os
from datetime import datetime
from werkzeug.utils import secure_filename

trades = Blueprint('trades', __name__)

@trades.route("/lot_calculator")
@login_required
def lot_calculator():
    from flask import session, jsonify
    from models import Account
    active_account_id = session.get('active_account_id')
    if not active_account_id:
        return jsonify({'error': 'No active account'}), 400
    
    account = Account.query.get(active_account_id)
    return jsonify({
        'balance': account.balance,
        'currency': 'USD'
    })

def calculate_trade_metrics(symbol, entry, exit, lots, trade_type):
    symbol = symbol.upper()
    diff = exit - entry if trade_type == 'Buy' else entry - exit
    
    # Defaults
    pip_size = 0.0001
    pip_value_per_lot = 10.0
    
    if "JPY" in symbol:
        pip_size = 0.01
        pip_value_per_lot = 9.1 # Dynamic calculation could be added here
    elif "XAU" in symbol or "GOLD" in symbol:
        pip_size = 0.01
        # Gold: $1 move = 100 pips = $100 per lot
        # So 1 pip (0.01 move) = $1 per lot
        pips = diff / 0.01
        pnl = diff * 100 * lots
        return round(pips, 2), round(pnl, 2), 1.0
    
    pips = diff / pip_size
    pnl = pips * pip_value_per_lot * lots
    
    return round(pips, 2), round(pnl, 2), pip_value_per_lot

@trades.route("/trades/new", methods=['GET', 'POST'])
@login_required
def new_trade():
    from flask import session
    active_account_id = session.get('active_account_id')
    if not active_account_id:
        flash('Please create/select an account first.', 'warning')
        return redirect(url_for('accounts.manage_accounts'))

    form = TradeForm()
    if form.validate_on_submit():
        pips, pnl, pip_val = calculate_trade_metrics(
            form.symbol.data, form.entry_price.data, form.exit_price.data, 
            form.lot_size.data, form.type.data
        )
        
        filename = None
        if form.screenshot.data:
            filename = secure_filename(form.screenshot.data.filename)
            form.screenshot.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
        trade = Trade(symbol=form.symbol.data, entry_price=form.entry_price.data,
                      exit_price=form.exit_price.data, lot_size=form.lot_size.data,
                      type=form.type.data, tag=form.tag.data, notes=form.notes.data,
                      screenshot=filename, pnl=pnl, pips=pips, pip_value=pip_val,
                      date=datetime.combine(form.date.data, datetime.now().time()), 
                      author=current_user, account_id=active_account_id)
        db.session.add(trade)
        db.session.commit()
        flash('Trade logged successfully!', 'success')
        return redirect(url_for('trades.trade_list'))
    return render_template('add_trade.html', form=form)

@trades.route("/trades")
@login_required
def trade_list():
    from flask import session
    active_account_id = session.get('active_account_id')
    all_trades = Trade.query.filter_by(user_id=current_user.id, account_id=active_account_id).order_by(Trade.date.desc()).all()
    return render_template('trades.html', trades=all_trades)

@trades.route("/trade/<int:trade_id>/delete", methods=['POST'])
@login_required
def delete_trade(trade_id):
    trade = Trade.query.get_or_404(trade_id)
    if trade.author != current_user: abort(403)
    db.session.delete(trade)
    db.session.commit()
    flash('Trade deleted.', 'success')
    return redirect(url_for('trades.trade_list'))
