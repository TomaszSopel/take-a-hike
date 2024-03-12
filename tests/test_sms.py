import unittest
from unittest.mock import patch
from sms import Sms

class TestSms(unittest.TestCase):
    """Tests sms.py functionality"""
    @patch("sms.Client")
    def test_send_message(self, mock_client):
        sms = Sms()

        sms.send_message("test")

        mock_client.return_value.messages.create.assert_called_once_with(
            from_='+18337970829',
            body="test",
            to='+18609673158',
        )