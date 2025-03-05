import event_db, sms, admin
class Text_message_input:
    """Creates Text_message_input object that can send messages via Twilio API"""
    def __init__(self, phone_number, body:str): # Initialization requires the phone number and message body from incoming text
        self.phone_number = phone_number.strip()
        self.body_list = [item.lower() for item in body.split()] # The message body string is split into a list of lowercase strings. 
                                                                 # This matches casing from within the postgres database.
    def process_text(self):
        """Takes the incoming phone number and message body and decides what functions to execute depending on incoming information"""
        if "signup" in self.body_list: # If 'signup' is found within message body
            events_list = event_db.get_events() # Gets a list of all events documented in the database
            if self.body_list[1] in events_list: # If the second word of the incoming text is found in the list of events...
                event_db.log_user(self.phone_number) # Logs the user into the users table if they're not already registered as a user
                user_id = event_db.get_user(self.phone_number) # Now that they're in the users table, get their corresponding user_id
                print(f"Process_text() user phone number is {self.phone_number} and user_id is {user_id}")
                event_id = event_db.get_event_id(self.body_list[1]) # Get the event_id that corresponds with the event they want to sign up for.
                # TODO: write a function that checks if the user is already signed up for an event
                messenger = sms.Sms() # Creates an Sms object used to send smsmsms
                result = event_db.sign_up(user_id=user_id, event_id=event_id)
                if result is None: # If they're already signed up, result = None
                    # TODO: Send the following message using event name instead of event code.
                    messenger.send_message(
                        f"You are already signed up for {self.body_list[1].capitalize()}!"
                        )
                elif result is True: # The signup function returns True if the user managed to sign up
                    messenger.send_message(
                        f"Signup for {self.body_list[1].capitalize()} confirmed!"
                        )
        elif "add" in self.body_list and admin.check_admin(self.phone_number) is True: # Functionality for if the first word of the text is 'add' which would be admin specific.
            if "admin" in self.body_list:
                print(f"{self.phone_number} is triggering me timbers! Their admin status is {admin.check_admin(self.phone_number)}")
"""Signing up:Text Cherry to 860-XXX-XXXX -->
Checks to see if your phone number is a part of the users table, 
if not, it will add it -->
Retreives the userID corresponding with the phone number
signs up the phone number for the particular event

Test curl command: curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/x-www-form-urlencoded" -d "Body=Signup Cherry" -d "From=18609673158"


"""


