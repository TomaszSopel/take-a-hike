import unittest
from unittest.mock import patch
from hike_api import app

# class TestReceiveText(unittest.TestCase):
#     """A class that tests receive_text()"""

#     @patch('hike_api.request')
#     def test_receive_text(self, mock_request):
#         mock_request.method = "POST"
#         mock_request.get_json().return_value = # INSERT TWILIO RESPONSE FORMAT HERE
        
#         receive_text()