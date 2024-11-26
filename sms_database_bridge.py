import event_db
class Text_message_input:
    """Creates Text_message_input object that can send messages via Twilio API"""
    def __init__(self, phone_number, body:str):
        self.phone_number = phone_number
        self.body_list = [item.lower() for item in body.split()]

    def process_text(self):
        if "signup" in self.body_list:
            events_list = event_db.get_events()
            if self.body_list[1] in events_list:
                print("I'm Triggered!")
            
"""Signing up:Text Cherry to 860-XXX-XXXX -->
Checks to see if your phone number is a part of the users table, if not, it will add it -->
Retreives the userID corresponding with the phone number
signs up the phone number for the particular event"""


text = Text_message_input('8609999999', "SIGNUP CHERRY")
text.process_text()
