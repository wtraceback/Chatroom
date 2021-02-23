from flask import url_for

from tests.base import BaseTestCase
from app import db
from app.models import User


class AdminTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        user = User(username='admin', email='admin@example.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def test_admin_permission(self):
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 403)

    def test_block_admin(self):
        self.login(username='admin', password='123456')
        response = self.client.delete(url_for('admin.block_user', user_id=2))
        self.assertEqual(response.status_code, 400)

    def test_block_user(self):
        self.login(username='admin', password='123456')
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(User.query.get(1))
