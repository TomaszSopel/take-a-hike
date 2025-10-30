import logging
import os

class Sms:
    """Creates Sms object that can send messages via Twilio API"""
    def __init__(self, twilio_client):
        self.client = twilio_client
        self.twilio_number = os.environ.get("TWILIO_NUMBER")
        if not self.twilio_number:
            logging.warning("TWILIO_NUMBER not found in environment variables!")
 
        
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

