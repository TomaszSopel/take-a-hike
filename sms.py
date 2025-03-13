from twilio.rest import Client
import os
import logging

class Sms:
    """Creates Sms object that can send messages via Twilio API"""
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.twilio_number = os.environ.get('TESTING_NUMBER')

        if self.account_sid and self.auth_token and self.twilio_number:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None 
            logging.error("Twilio credentials not set")
        
# TODO: Modify the send message function to require a phone number as an argument (otherwise all followup texts following a signup will be sent to the twilio number)
    def send_sms(self, to_number, body):
        #TODO: The send_message function can only send messages to the hard coded phone number, add a parameter in the initialization of the Sms object to include the senders phone number such that they can get the response sent to their number. 
        
        if not to_number:
            to_number = os.environ.get('TESTING_NUMBER')
        
        self.client.messages.create(
            from_=os.environ.get('TWILIO_NUMBER'),
            body=body,
            to=to_number,
            )
        logging.info("Sent text")

