import textreminder
import unittest
from unittest.mock import patch


class TextReminderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = textreminder.app.test_client()

    def test_main(self):
        response =  self.app.get('/')

    @patch('messaging.SMTP.send_message')
    def test_register_task(self, send_message):
        number = '1234567890'
        carrier = 'T-Mobile'
        message = 'Test Message'
        self.app.post('/task', data=dict(
            number=number,
            carrier=carrier,
            message=message
        ))
        (email,), _ = send_message.call_args
        assert email['To'] == number+'@tmomail.net'


if __name__ == '__main__':
    unittest.main()
