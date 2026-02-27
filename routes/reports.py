from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Trade

reports = Blueprint('reports', __name__)

@reports.route("/reports")
@login_required
def reports_view():
    from flask import session
    active_account_id = session.get('active_account_id')
    if not active_account_id:
        return redirect(url_for('accounts.manage_accounts'))

    all_trades = Trade.query.filter_by(user_id=current_user.id, account_id=active_account_id).all()
    total_trades = len(all_trades)
    wins = [t for t in all_trades if t.pnl > 0]
    win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
    total_pnl = sum([t.pnl for t in all_trades])
    total_pips = sum([t.pips or 0 for t in all_trades])
    avg_pips = (total_pips / total_trades) if total_trades > 0 else 0
    
    return render_template('reports.html', total_trades=total_trades, win_rate=win_rate, 
                           total_pnl=total_pnl, total_pips=total_pips, avg_pips=avg_pips)
