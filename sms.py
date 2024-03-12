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
            from_='+18337970829',
            body=msg,
            to='+18609673158',
            )
        logging.info("Sent text")

