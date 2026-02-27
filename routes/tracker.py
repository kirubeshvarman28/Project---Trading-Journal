from flask import Blueprint, render_template
from flask_login import login_required

tracker = Blueprint('tracker', __name__)

@tracker.route("/tracker")
@login_required
def progress():
    return render_template('tracker.html')
