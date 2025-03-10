from twilio.rest import Client
import os
import logging

class Sms:
    """Creates Sms object that can send messages via Twilio API"""
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)
# TODO: Modify the send message function to require a phone number as an argument (otherwise all followup texts following a signup will be sent to the twilio number)
    def send_message(self, msg):
        #TODO: The send_message function can only send messages to the hard coded phone number, add a parameter in the initialization of the Sms object to include the senders phone number such that they can get the response sent to their number. 
        self.client.messages.create(
            from_=os.environ.get('TWILIO_NUMBER'),
            body=msg,
            to=os.environ.get('TESTING_NUMBER'),
            )
        logging.info("Sent text")

