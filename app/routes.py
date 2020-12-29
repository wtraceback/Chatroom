from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
def index():
    title = 'Chatroom'

    return render_template('index.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me = {}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)
