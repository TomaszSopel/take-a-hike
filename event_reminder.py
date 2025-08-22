import datetime
import logging
import event_db
from sms import Sms
from twilio.rest import Client
import os

class EventReminderService:
    def __init__(self):
        self.twilio_client = Client(
            os.environ.get('TWILIO_SID'),
            os.environ.get('TWILIO_AUTH_TOKEN')
        )
        self.sms = Sms(self.twilio_client)
        self.confirmation_requests = {}
        self.scheduler_running = False
        
    def check_and_send_reminders(self):
        """Check for tomorrow's events and send confirmation requests"""
        try:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            events = event_db.get_events_for_date(tomorrow)
            
            if not events:
                logging.info(f"No events scheduled for {tomorrow}")
                return
                
            logging.info(f"Found {len(events)} events for {tomorrow}")
            
            for event in events:
                self.send_event_reminders(event)
                
        except Exception as e:
            logging.error(f"Error in check_and_send_reminders: {e}")
    
    