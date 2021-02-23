from flask import url_for, current_app

from app import db, socketio
from app.models import User, Message
from tests.base import BaseTestCase


class ChatTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        admin = User(username='admin', email='admin@example.com', github='https://github.com/wtraceback')
        admin.set_password('123456')
        msg1 = Message(body='test message 1')
        msg2 = Message(body='test message 2')
        msg3 = Message(body='test message 3')
        admin.messages = [msg1, msg2, msg3]
        db.session.add(admin)
        db.session.commit()

    def test_index_page(self):
        response = self.client.get(url_for('chat.index'))
        data = response.get_data(as_text=True)
        self.assertIn('test message 1', data)
        self.assertIn('test message 2', data)
        self.assertIn('test message 3', data)

    def test_get_messages(self):
        current_app.config['CHATROOM_MESSAGE_PER_PAGE'] = 1
        response = self.client.get(url_for('chat.index'))
        data = response.get_data(as_text=True)
        self.assertIn('test message 3', data)
        self.assertNotIn('test message 1', data)
        self.assertNotIn('test message 2', data)

        response = self.client.get(url_for('chat.get_messages', page=1))
        data = response.get_data(as_text=True)
        self.assertIn('test message 3', data)
        self.assertNotIn('test message 1', data)
        self.assertNotIn('test message 2', data)

        response = self.client.get(url_for('chat.get_messages', page=2))
        data = response.get_data(as_text=True)
        self.assertIn('test message 2', data)
        self.assertNotIn('test message 1', data)
        self.assertNotIn('test message 3', data)

        response = self.client.get(url_for('chat.get_messages', page=3))
        data = response.get_data(as_text=True)
        self.assertIn('test message 1', data)
        self.assertNotIn('test message 2', data)
        self.assertNotIn('test message 3', data)

    def test_get_profile(self):
        response = self.client.get(url_for('chat.get_profile', user_id=2))
        data = response.get_data(as_text=True)
        self.assertIn('https://github.com/wtraceback', data)
        self.assertIn('This user want to maintain an aura of mystique.', data)

    def test_edit_profile(self):
        self.login(username='admin', password='123456')
        self.client.post(url_for('chat.profile'), data={
            'github': 'https://github.com/wtraceback/Chatroom',
            'website': 'https://github.com/wtraceback/Watchlist',
            'bio': 'test edit profile...'
        }, follow_redirects=True)

        response = self.client.get(url_for('chat.get_profile', user_id=2))
        data = response.get_data(as_text=True)
        self.assertIn('https://github.com/wtraceback/Chatroom', data)
        self.assertIn('https://github.com/wtraceback/Watchlist', data)
        self.assertIn('test edit profile...', data)
        self.assertNotIn('This user want to maintain an aura of mystique.', data)

    def test_delete_message(self):
        self.login(username='admin', password='123456')

        response = self.client.delete(url_for('chat.delete_message', message_id=1))
        self.assertEqual(response.status_code, 204)

        response = self.client.get(url_for('chat.index'))
        data = response.get_data(as_text=True)
        self.assertNotIn('test message 1', data)
        self.assertIn('test message 2', data)
        self.assertIn('test message 3', data)

        user = User.query.get(1)
        msg = Message(body='test message 4')
        user.messages.append(msg)
        db.session.commit()

        response = self.client.delete(url_for('chat.delete_message', message_id=4))
        self.assertEqual(response.status_code, 204)

        response = self.client.get(url_for('chat.index'))
        data = response.get_data(as_text=True)
        self.assertNotIn('test message 4', data)
        self.assertIn('test message 2', data)
        self.assertIn('test message 3', data)

        self.logout()
        self.login()

        response = self.client.delete(url_for('chat.delete_message', message_id=2))
        self.assertEqual(response.status_code, 403)
