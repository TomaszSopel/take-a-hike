import event_db, admin

class SignupCommand:
    """Handles the signup command."""
    def __init__(self, phone_number, event_code):
        self.phone_number = phone_number
        self.event_code = event_code

    def execute(self):
        events_list = event_db.get_events() # Gets a list of all events documented in the database
        print(f"Execute() triggered, but before if statement, events_list is {events_list}")
        if self.event_code in events_list: # If the second word of the incoming text is found in the list of events...
            event_db.log_user(self.phone_number) # Logs the user into the users table if they're not already registered as a user
            user_id = event_db.get_user(self.phone_number) # Now that they're in the users table, get their corresponding user_id
            print(f"Process_text() user phone number is {self.phone_number} and user_id is {user_id}")
            event_id = event_db.get_event_id(self.event_code) # Get the event_id that corresponds with the event they want to sign up for.
            # TODO: write a function that checks if the user is already signed up for an event
            result = event_db.sign_up(user_id=user_id, event_id=event_id)
            print(result)
            if result is None: # If they're already signed up, result = None
                # TODO: Send the following message using event name instead of event code.
                return f"You are already signed up for {self.event_code.capitalize()}!"        
            elif result is True: # The signup function returns True if the user managed to sign up
                return f"Signup for {self.event_code.capitalize()} confirmed!"

commands = {
    "signup": SignupCommand,
}

def process_sms(phone_number, message_body):
    """Processes the incoming text and executes the related commands on the database."""
    message_body_list = message_body.strip().lower().split()
    if not message_body:
        return "Empty Message Body"
    
    command_keyword = message_body_list[0] #Command keyword == *signup* cherry, triggers what function is executed
    command_args = message_body_list[1] # Command_args == signup *cherry*, provides arguments for specific function

    command_name = commands.get(command_keyword)

    if command_name:
        try:
            if command_keyword == "signup" and command_args:
                command_response = command_name(phone_number, command_args)
                return command_response.execute()
        except Exception as e:
            print(f"Error in signup: {e}")
            return(f"Error in signup: {e}")
"""
Test curl command: 
curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/x-www-form-urlencoded" -d "Body=Signup Cherry" -d "From=18609673158"
"""


