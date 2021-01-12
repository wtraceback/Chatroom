from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.chat import chat_bp
from app.models import User, Message
from app.forms import ProfileForm


@chat_bp.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/index.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        github = form.github.data
        website = form.website.data
        bio = form.bio.data
        print('github = {}, website = {}, bio = {}'.format(github, website, bio))

        current_user.github = github
        current_user.website = website
        current_user.bio = bio
        db.session.commit()
        return redirect(url_for('chat.index'))

    form.github.data = current_user.github
    form.website.data = current_user.website
    form.bio.data = current_user.bio
    return render_template('chat/profile.html', form=form)
