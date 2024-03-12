from twilio.rest import Client
import os
import logging

class Sms:
    """Creates Sms object that can send messages via Twilio API"""
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, msg):
        message = self.client.messages.create(
            from_=os.environ.get('TWILIO_NUMBER'),
            body=msg,
            to=os.environ.get('TESTING_NUMBER'),
            )
        logging.info("Sent text")

