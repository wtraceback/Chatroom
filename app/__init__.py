import os
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])
config[config_name].init_app(app)
db = SQLAlchemy(app)
login = LoginManager(app)


from app.auth import auth_bp
app.register_blueprint(auth_bp)
from app.chat import chat_bp
app.register_blueprint(chat_bp)
from app.errors import errors_bp
app.register_blueprint(errors_bp)


login.login_view = 'auth.login'
login.login_message = 'Please log in'

@login.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id))


from app import models
