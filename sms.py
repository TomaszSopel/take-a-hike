from twilio.rest import Client
import os

class Sms:
    def __init__(self):
        self.account_sid = os.environ['TWILIO_SID'] 
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, msg):
        message = self.client.messages.create(
            from_='+18337970829',
            body=msg,
            to='+18609673158'
)

