import os
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect


db = SQLAlchemy()
login = LoginManager()
csrf = CSRFProtect()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_extensions(app)
    register_blueprints(app)

    return app


login.login_view = 'auth.login'
login.login_message = 'Please log in'

@login.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id))


def register_extensions(app):
    db.init_app(app)
    login.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.chat import chat_bp
    app.register_blueprint(chat_bp)
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)
