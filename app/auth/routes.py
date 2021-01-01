from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.auth import auth_bp


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('chat.index')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('chat.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
