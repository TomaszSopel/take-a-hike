import unittest
from unittest.mock import patch
from hike_api import hello_world

class TestSmsFunctionality(unittest.TestCase):

    @patch('hike_api.Sms')  # Mock the Sms class
    def test_send_message_called(self, mock_sms):
        hello_world()  # Call the endpoint function

        # Assert that Sms object was created
        mock_sms.assert_called_once() 

        # Assert that send_message was called on the mock
        mock_sms.return_value.send_message.assert_called_once_with("Get Message Sent")