import os
import click
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
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
    register_template_context(app)
    register_commands(app)

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


def register_template_context(app):
    from app.models import User

    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            user_id = current_user.get_id()
            active_user = User.query.get(user_id)
        else:
            active_user = None

        return dict(active_user=active_user)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""

        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')

        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--message', default=100, help='Quantity of messages, default is 100.')
    def forge(message):
        """Generate fake data."""
        from app.models import User, Message
        from faker import Faker
        import random
        from sqlalchemy.exc import IntegrityError

        fake = Faker()

        click.echo('Initializing the database...')
        db.drop_all()
        db.create_all()

        click.echo('Forging the data...')
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()

        click.echo('Generating users...')
        for i in range(50):
            user = User(username=fake.name(), email=fake.email())
            db.session.add(user)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        click.echo('Generating messages...')
        for i in range(message):
            msg = Message(
                body=fake.sentence(),
                author=User.query.get(random.randint(1, User.query.count())),
                timestamp=fake.date_time_this_year()
            )
            db.session.add(msg)

        db.session.commit()
        click.echo('Done.')
