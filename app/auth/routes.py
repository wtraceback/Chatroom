from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.models import User
from app.auth import auth_bp


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me', False)

        if remember_me:
            remember_me = True

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user, remember_me)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('chat.index')
            return redirect(next_page)

        flash('Invalid username or password')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        is_exists = False
        if user is not None:
            flash('Please use a different username.')
            is_exists = True

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('Please use a different email address.')
            is_exists = True

        if is_exists:
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
