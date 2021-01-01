from flask import render_template
from flask_login import login_required
from app.chat import chat_bp


@chat_bp.route('/')
@login_required
def index():
    title = 'Chatroom'

    return render_template('chat/index.html', title=title)
