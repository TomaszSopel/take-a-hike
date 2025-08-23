import schedule
import time
import datetime
import threading
import logging
from typing import Dict
import event_db
import admin
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
    
    def send_event_reminders(self, event: Dict):
        """Send reminder SMS to all signed up users for an event"""
        try:
            event_id = event['event_id']
            event_name = event['event_name']
            
            signed_up_users = event_db.event_get_numbers(event_id)
            
            if not signed_up_users:
                logging.info(f"No users signed up for event: {event_name}")
                return
                
            confirmation_id = f"{event_id}_{int(time.time())}"
            self.confirmation_requests[confirmation_id] = {
                'event_id': event_id,
                'event_name': event_name,
                'total_signups': len(signed_up_users),
                'confirmations': 0,
                'start_time': datetime.datetime.now()
            }
            
            message = f"Hi! You're signed up for {event_name} tomorrow. Reply 'CONFIRM {confirmation_id}' to confirm your attendance."
            
            for user_tuple in signed_up_users:
                user_id = user_tuple[0]
                phone_number = event_db.get_phone(user_id)
                
                if phone_number and phone_number != 0:
                    try:
                        self.sms.send_sms(phone_number, message)
                        logging.info(f"Sent reminder to {phone_number} for {event_name}")
                    except Exception as e:
                        logging.error(f"Failed to send SMS to {phone_number}: {e}")
                        
            threading.Timer(14400, self.send_admin_report, args=[confirmation_id]).start()
            logging.info(f"Scheduled admin report for {event_name} in 4 hours")
            
        except Exception as e:
            logging.error(f"Error sending event reminders: {e}")
    
    