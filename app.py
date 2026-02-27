from flask import Flask
from config import Config
from models import db, login_manager, User
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.accounts import accounts
    from routes.auth import auth
    from routes.trades import trades
    from routes.dashboard import main
    from routes.journal import journal
    from routes.reports import reports
    from routes.notebook import notebook
    from routes.playbooks import playbooks
    from routes.resources import resources
    from routes.tracker import tracker
    from routes.replay import replay

    app.register_blueprint(accounts)
    app.register_blueprint(auth)
    app.register_blueprint(trades)
    app.register_blueprint(main)
    app.register_blueprint(journal)
    app.register_blueprint(reports)
    app.register_blueprint(notebook)
    app.register_blueprint(playbooks)
    app.register_blueprint(resources)
    app.register_blueprint(tracker)
    app.register_blueprint(replay)

    @app.context_processor
    def inject_accounts():
        from flask_login import current_user
        from flask import session
        from models import Account
        if current_user.is_authenticated:
            user_accounts = Account.query.filter_by(user_id=current_user.id).all()
            active_account_id = session.get('active_account_id')
            active_account = None
            if active_account_id:
                active_account = Account.query.get(active_account_id)
            if not active_account and user_accounts:
                active_account = user_accounts[0]
                session['active_account_id'] = active_account.id
            return dict(user_accounts=user_accounts, active_account=active_account)
        return dict(user_accounts=[], active_account=None)

    with app.app_context():
        db.create_all()
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
