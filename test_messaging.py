import messaging
import unittest
from unittest.mock import patch


class MessagingTestCase(unittest.TestCase):

    @patch('messaging.SMTP.send_message')
    def test_send_message(self, send_message):
        messaging.send_message('', '')
        assert send_message.called


if __name__ == '__main__':
    unittest.main()
