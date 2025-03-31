import unittest
import os
from unittest.mock import patch, MagicMock
from sms import Sms

TEST_RECIPIENT_NUMBER = os.environ.get('TWILIO_NUMBER', '+123456789')
TEST_MESSAGE_BODY = "THIS IS A REALLY LOUD MESSAGE"

class TestSms(unittest.TestCase):
    """Tests sms.py functionality"""
    @patch("sms.Client")
    def test_send_sms(self, MockTwilioClient):
        mock_client_instance = MockTwilioClient.return_value # The INSTANCE mock
        mock_message = MagicMock()
        mock_message.sid = "SMS Test Message"
        mock_client_instance.messages.create.return_value = mock_message

        sms_sender = Sms(mock_client_instance)

        result_sid = sms_sender.send_sms(to_number=TEST_RECIPIENT_NUMBER, body=TEST_MESSAGE_BODY)

        mock_client_instance.messages.create.assert_called_once_with(
            from_=os.environ.get('TWILIO_NUMBER'), # Still need TWILIO_NUMBER env var for from_
            body=TEST_MESSAGE_BODY,
            to=TEST_RECIPIENT_NUMBER
        )
        self.assertEqual(result_sid, "SMS Test Message")