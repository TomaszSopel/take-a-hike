import datetime
import logging
import os
import threading
import time
from typing import Dict

import schedule
from twilio.rest import Client

import admin
import event_db
from sms import Sms


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
            event_code = event['event_code']
            
            signed_up_users = event_db.get_user_ids_for_event(event_id)
            
            if not signed_up_users:
                logging.info(f"No users signed up for event: {event_name}")
                return
                
            confirmation_id = f"{event_id}_{int(time.time())}"
            self.confirmation_requests[confirmation_id] = {
                'event_id': event_id,
                'event_name': event_name,
                'total_signups': len(signed_up_users),
                'start_time': datetime.datetime.now()
            }
            
            message = f"Hi! You're signed up for {event_name} tomorrow. Reply 'CONFIRM {event_code}' to confirm your attendance."
            
            for user in signed_up_users:
                phone_number = event_db.get_phone(user)
                
                if phone_number:
                    try:
                        self.sms.send_sms(phone_number, message)
                        logging.info(f"Sent reminder to {phone_number} for {event_name}")
                    except Exception as e:
                        logging.error(f"Failed to send SMS to {phone_number}: {e}")
                        
            threading.Timer(14400, self.send_admin_headcount_report, args=[confirmation_id]).start()
            logging.info(f"Scheduled admin report for {event_name} in 4 hours")
            
        except Exception as e:
            logging.error(f"Error sending event reminders: {e}")

    def send_admin_headcount_report(self, confirmation_id):
        """Sends the final headcount report to admins."""
        event_id = int(confirmation_id.split("_")[0]) #Confirmation ID is a string containing eventID_timestamp
        
        event_data = self.confirmation_requests[confirmation_id]

        event_name = event_data["event_name"]
        admin_numbers = admin.get_admins()
        headcount = admin.get_confirmation_count(event_id)
        total_signups = event_data["total_signups"]

        message = f"The headcount for tomorrow's {event_name} is {headcount}/{total_signups} signups!"

        for admin_phone_number in admin_numbers:
            self.sms.send_sms(to_number=admin_phone_number, body=message)
