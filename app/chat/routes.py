from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.chat import chat_bp
from app.models import User, Message


@chat_bp.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/index.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        github = request.form['github']
        website = request.form['website']
        bio = request.form['bio']

        current_user.github = github
        current_user.website = website
        current_user.bio = bio
        db.session.commit()
        return redirect(url_for('chat.index'))

    return render_template('chat/profile.html')
