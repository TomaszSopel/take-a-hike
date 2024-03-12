import unittest
from unittest.mock import patch
from hike_api import hello_world, receive_text

class TestHelloWorld(unittest.TestCase):
    """A class that tests hello_world()"""

    @patch('hike_api.Sms')
    def test_hello_world(self, mock_sms):
        hello_world()
        mock_sms.assert_called_once()
        mock_sms.return_value.send_message.assert_called_once_with("Get Message Sent")

# class TestReceiveText(unittest.TestCase):
#     """A class that tests receive_text()"""

#     @patch('hike_api.request')
#     def test_receive_text(self, mock_request):
#         mock_request.method = "POST"
#         mock_request.get_json().return_value = # INSERT TWILIO RESPONSE FORMAT HERE
        
#         receive_text()