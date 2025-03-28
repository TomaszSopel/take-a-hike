import unittest
from unittest.mock import patch
from hike_api import hello_world, app

class TestHelloWorld(unittest.TestCase):
    """A class that tests hello_world()"""
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    @patch('hike_api.Sms')
    def test_hello_world(self, mock_sms_class):
        response = self.client.get('/') 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello World!") # Check the response body


# class TestReceiveText(unittest.TestCase):
#     """A class that tests receive_text()"""

#     @patch('hike_api.request')
#     def test_receive_text(self, mock_request):
#         mock_request.method = "POST"
#         mock_request.get_json().return_value = # INSERT TWILIO RESPONSE FORMAT HERE
        
#         receive_text()