from flask import url_for

from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Sign In', data)

    def test_fail_login(self):
        response = self.login(username='test123', password='123456')
        data = response.get_data(as_text=True)
        self.assertIn('Invalid username or password', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertNotIn('Sign Out', data)
        self.assertIn('Sign In', data)

    def test_login_protect(self):
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('Please log in', data)

    def test_register(self):
        response = self.client.post(url_for('auth.register'), data={
            'username': 'test1',
            'email': 'test1@example.com',
            'password': '123456'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Congratulations, you are now a registered user!', data)

    def test_register_username_exist(self):
        response = self.client.post(url_for('auth.register'), data={
            'username': 'test',
            'email': 'test7@example.com',
            'password': '123456'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Please use a different username.', data)

    def test_register_email_exist(self):
        response = self.client.post(url_for('auth.register'), data={
            'username': 'test7',
            'email': 'test@example.com',
            'password': '123456'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Please use a different email address.', data)
