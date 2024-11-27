import event_db, sms
class Text_message_input:
    """Creates Text_message_input object that can send messages via Twilio API"""
    def __init__(self, phone_number, body:str):
        self.phone_number = phone_number
        self.body_list = [item.lower() for item in body.split()]

    def process_text(self):
        if "signup" in self.body_list:
            events_list = event_db.get_events()
            if self.body_list[1] in events_list:
                event_db.log_user(self.phone_number)
                user_id = event_db.get_user(self.phone_number)
                event_id = event_db.get_event_id(self.body_list[1])
                # TODO: write a function that checks if the user is already signed up for an event
                event_db.sign_up(user_id=user_id, event_id=event_id)
                # TEMP CODE TO CONFIRM sign-up (these texts can ONLY be sent to the twilio number atm.)
                messenger = sms.Sms()
                messenger.send_message(f"Signup for {self.body_list[1].capitalize()} confirmed!")

            
"""Signing up:Text Cherry to 860-XXX-XXXX -->
Checks to see if your phone number is a part of the users table, if not, it will add it -->
Retreives the userID corresponding with the phone number
signs up the phone number for the particular event"""

