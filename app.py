from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        from routes import auth_bp, main_bp, dashboard_bp, note_bp, circle_bp, admin_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(note_bp)
        app.register_blueprint(circle_bp)
        app.register_blueprint(admin_bp)
        db.create_all()

    return app
