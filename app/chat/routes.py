from flask import render_template, redirect, url_for, request, flash, current_app, abort
from flask_login import login_required, current_user
from flask_socketio import emit
from app import db, socketio
from app.chat import chat_bp
from app.models import User, Message
from app.utils import to_html

online_users = []


@chat_bp.route('/')
def index():
    per_page = current_app.config['CHATROOM_MESSAGE_PER_PAGE']
    messages = Message.query.order_by(Message.timestamp.asc())[-per_page:]
    user_amount = User.query.count()
    return render_template('chat/index.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/messages')
def get_messages():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['CHATROOM_MESSAGE_PER_PAGE']
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page, per_page, True)
    messages = pagination.items
    return render_template('chat/_messages.html', messages=messages[::-1])


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


@chat_bp.route('/profile/<user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('chat/_profile_card.html', user=user)


@chat_bp.route('/message/delete/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if current_user != message.author and not current_user.is_admin:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    return '', 204


@socketio.on('new message')
def new_message(msg):
    html_message = to_html(msg['data'])
    message = Message(author=current_user._get_current_object(), body=html_message)
    db.session.add(message)
    db.session.commit()
    emit('new message',
        {
            'data': render_template('chat/_message.html', message=message),
            'body': html_message,
            'gravatar': current_user.avatar(128),
            'username': current_user.username,
            'user_id': current_user.id
        },
        broadcast=True
    )


@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('online users', {'data': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('online users', {'data': len(online_users)}, broadcast=True)
