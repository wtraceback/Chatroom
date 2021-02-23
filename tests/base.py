import os

os.environ['GITHUB_CLIENT_ID']='test'
os.environ['GITHUB_CLIENT_SECRET']='test'

import unittest
from flask import url_for

from app import create_app, db
from app.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.test_request_context()
        self.context.push()

        # 创建测试客户端
        self.client = self.app.test_client()
        # 创建测试命令运行器
        self.runner = self.app.test_cli_runner()

        db.create_all()
        user = User(username='test', email='test@example.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username='test'
            password='123456'

        return self.client.post(url_for('auth.login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)
