from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)


login.login_view = 'login'
login.login_message = 'Please log in'

@login.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id))


from app import routes, models
