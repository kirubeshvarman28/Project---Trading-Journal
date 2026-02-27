from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Trade
import calendar
from datetime import datetime, date

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/dashboard")
@login_required
def dashboard():
    from flask import session
    active_account_id = session.get('active_account_id')
    if not active_account_id:
        return redirect(url_for('accounts.manage_accounts'))
    
    all_trades = Trade.query.filter_by(user_id=current_user.id, account_id=active_account_id).order_by(Trade.date.asc()).all()
    
    total_trades = len(all_trades)
    total_pnl = sum([t.pnl for t in all_trades])
    wins = [t for t in all_trades if t.pnl > 0]
    win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
    
    # Advanced Metrics
    losses = [t for t in all_trades if t.pnl <= 0]
    gross_profit = sum([t.pnl for t in wins])
    gross_loss = abs(sum([t.pnl for t in losses]))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (gross_profit if gross_profit > 0 else 0)
    
    avg_win = (gross_profit / len(wins)) if wins else 0
    avg_loss = (gross_loss / len(losses)) if losses else 0
    expectancy = ((win_rate/100) * avg_win) - ((1 - win_rate/100) * avg_loss)
    
    # Radar Metrics Logic (Simplified for Demo)
    consistency = 95.0 if total_trades > 5 else 0
    avg_win_loss_ratio = (avg_win / avg_loss * 50) if avg_loss > 0 else 50 # Scaled to 0-100 radar
    recovery_factor = 100.0 if total_pnl > 0 else 0
    max_dd = 80.0 if total_pnl < 0 else 100.0 # Better score for less DD
    
    radar_data = [
        win_rate,
        min(profit_factor * 10, 100), # Cap for visual
        min(avg_win_loss_ratio, 100),
        recovery_factor,
        max_dd,
        consistency
    ]
    zella_score = sum(radar_data) / 6

    # Chart Data: Cumulative & Daily
    cumulative_data = []
    daily_data = []
    current_cum_pnl = 0
    
    # Group by day first
    daily_stats = {}
    for t in all_trades:
        d_str = t.date.strftime('%Y-%m-%d')
        if d_str not in daily_stats: daily_stats[d_str] = 0
        daily_stats[d_str] += t.pnl

    sorted_days = sorted(daily_stats.keys())
    for d_str in sorted_days:
        day_pnl = daily_stats[d_str]
        current_cum_pnl += day_pnl
        cumulative_data.append({'x': d_str, 'y': current_cum_pnl})
        daily_data.append({'x': d_str, 'y': day_pnl})

    # Calendar Data with Weekly Summaries
    today = date.today()
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(today.year, today.month)
    
    calendar_data = []
    weekly_summaries = []
    for week in month_days:
        week_data = []
        week_pnl = 0
        week_trades = 0
        for d in week:
            if d == 0: week_data.append(None)
            else:
                ds = f"{today.year}-{today.month:02d}-{d:02d}"
                stats = {'pnl': daily_stats.get(ds, 0), 'count': 1 if ds in daily_stats else 0}
                week_data.append({'day': d, 'stats': stats})
                week_pnl += stats['pnl']
                week_trades += stats['count']
        
        calendar_data.append(week_data)
        weekly_summaries.append({'pnl': week_pnl, 'days': week_trades})

    recent_trades = all_trades[-10:][::-1]
    
    avg_pips = (sum([t.pips for t in all_trades]) / total_trades) if total_trades > 0 else 0
    best_trade = max(all_trades, key=lambda t: t.pnl) if all_trades else None
    
    return render_template('dashboard.html', 
                           total_pnl=total_pnl, win_rate=win_rate,
                           profit_factor=profit_factor, expectancy=expectancy,
                           avg_pips=avg_pips, best_trade=best_trade,
                           radar_data=radar_data, zella_score=zella_score,
                           cumulative_pnl=cumulative_data, daily_pnl=daily_data,
                           calendar_data=calendar_data, weekly_summaries=weekly_summaries,
                           month_name=today.strftime('%B %Y'),
                           recent_trades=recent_trades)
