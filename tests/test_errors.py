from tests.base import BaseTestCase


class ErrorsTestCase(BaseTestCase):

    def test_404_error(self):
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Chatroom - 404', data)
