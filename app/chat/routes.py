from flask import render_template
from flask_login import login_required
from app.chat import chat_bp
from app.models import User, Message


@chat_bp.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/index.html', messages=messages, user_amount=user_amount)
