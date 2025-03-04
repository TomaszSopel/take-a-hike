import event_db, sms
class Text_message_input:
    """Creates Text_message_input object that can send messages via Twilio API"""
    def __init__(self, phone_number, body:str):
        self.phone_number = phone_number.strip()
        self.body_list = [item.lower() for item in body.split()]

    def process_text(self):
        if "signup" in self.body_list:
            events_list = event_db.get_events()
            print(events_list)
            if self.body_list[1] in events_list:
                event_db.log_user(self.phone_number)
                user_id = event_db.get_user(self.phone_number)
                print(f"Process_text() user phone number is {self.phone_number} and user_id is {user_id}")
                event_id = event_db.get_event_id(self.body_list[1])
                # TODO: write a function that checks if the user is already signed up for an event
                messenger = sms.Sms()
                result = event_db.sign_up(user_id=user_id, event_id=event_id)
                print(f"result = {result}")
                if result is None:
                    # TODO: Send the following message using event name instead of event code.
                    messenger.send_message(
                        f"You are already signed up for {self.body_list[1].capitalize()}!"
                        )
                elif result is True:
                    messenger.send_message(
                        f"Signup for {self.body_list[1].capitalize()} confirmed!"
                        )
        elif "add" in self.body_list:
            if "admin" in self.body_list:
                print(f"{self.phone_number} is triggering me timbers!")
"""Signing up:Text Cherry to 860-XXX-XXXX -->
Checks to see if your phone number is a part of the users table, 
if not, it will add it -->
Retreives the userID corresponding with the phone number
signs up the phone number for the particular event

Test curl command: curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/x-www-form-urlencoded" -d "Body=Signup Cherry" -d "From=18609673158"


"""


