from app import db
from app.models import User, Message

from tests.base import BaseTestCase


class CLITestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        db.drop_all()

    def test_initdb_command(self):
        result = self.runner.invoke(args=['initdb'])
        self.assertIn('Initialized database.', result.output)

    def test_initdb_command_with_drop(self):
        result = self.runner.invoke(args=['initdb', '--drop'], input='y\n')
        self.assertIn('This operation will delete the database, do you want to continue?', result.output)
        self.assertIn('Drop tables.', result.output)

    def test_forge_command(self):
        result = self.runner.invoke(args=['forge'])

        self.assertEqual(User.query.count(), 50 + 1)
        self.assertIn('Generating users...', result.output)

        self.assertEqual(Message.query.count(), 100)
        self.assertIn('Generating messages...', result.output)

        self.assertIn('Done.', result.output)

    def test_forge_command_with_count(self):
        result = self.runner.invoke(args=['forge', '--message', '60'])

        self.assertEqual(Message.query.count(), 60)
        self.assertIn('Generating messages...', result.output)

        self.assertIn('Done.', result.output)
