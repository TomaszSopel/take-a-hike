from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import logging

class Sms:
    """Creates Sms object that can send messages via Twilio API"""
    def __init__(self, twilio_client):
        self.client = twilio_client
        self.twilio_number = os.environ.get("TWILIO_NUMBER")
        if not self.twilio_number:
            logging.warning("TWILIO_NUMBER not found in environment variables!")
        # self.account_sid = os.environ.get('TWILIO_SID')
        # self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        # self.twilio_number = os.environ.get('TESTING_NUMBER')

        # if self.account_sid and self.auth_token and self.twilio_number:
        #     self.client = Client(self.account_sid, self.auth_token)
        # else:
        #     self.client = None 
        #     logging.error("Twilio credentials not set")
        
# TODO: Modify the send message function to require a phone number as an argument (otherwise all followup texts following a signup will be sent to the twilio number)
    def send_sms(self, to_number, body):
        try:
            message = self.client.messages.create(
                to = to_number,
                from_ = self.twilio_number,
                body = body
            )
            return message.sid
        except Exception as e:
            logging.error(f"Error sending SMS: {e}")

        # self.client.messages.create(
        #     from_=os.environ.get('TWILIO_NUMBER'),
        #     body=body,
        #     to=to_number,
        #     )
        # logging.info("Sent text")

