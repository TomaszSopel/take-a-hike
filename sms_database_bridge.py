import event_db, admin

class SignupCommand:
    """Handles the signup command."""
    def __init__(self, phone_number, event_code):
        self.phone_number = phone_number
        self.event_code = event_code

    def execute(self):
        try:
            event = event_db.get_event_by_code(self.event_code) # Retrieves all relevant data for the event based on the event code
            
            if not event: # Returns an error message if the event code is not found
                return f"Event '{self.event_code}' not found. Please check the code and try again."

            user_id = event_db.get_user(self.phone_number)

            if not user_id:
                event_db.log_user(self.phone_number) #If not found, log the user
                user_id = event_db.get_user(self.phone_number) # Retrieve the user id after logging the user
                if not user_id:
                    return "Error: Unable to find or create user_ID, please contact Admin."            
            result = event_db.sign_up(user_id=user_id, event_id=event['event_id'])

            if result is None:
                return f"You are already signed up for {event['event_name']}."
            elif result is True:
                return f"Signup for {event['event_name']} confirmed!"
            else: # Handles if sign_up returns False (e.g., from an error)
                return "Signup failed due to a database issue."
        except Exception as error:
            print(f"Error in SignupCommand.execute: {error}")
            return "Error (Signup)"

class CancelCommand:
    """Handles the cancel command."""
    def __init__(self, phone_number, event_code):
        self.phone_number = phone_number
        self.event_code = event_code

    def execute(self):
        """Executes the cancel command, removing the user from the event registration."""
        try:
            event = event_db.get_event_by_code(self.event_code)
            if not event:
                return f"Event {self.event_code} not found."
            
            user_id = event_db.get_user(self.phone_number)
            if not user_id:
                return f"You were not signed up for {event['event_name']}."
            
            was_cancelled = event_db.cancel_signup(user_id, event['event_id'])
            if was_cancelled:
                return f"Your signup for {event['event_name']} has been cancelled."
            else:
                return f"You were not signed up for {event['event_name']}."
        except Exception as error:
            print(f"Error in CancelCommand.execute: {error}")
            return "An error occured while trying to cancel your signup."


"""
Test curl command: 
curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/x-www-form-urlencoded" -d "Body=Signup Cherry" -d "From=18609673158"
"""


# Dictionary of all commands
commands = {
    "signup": SignupCommand,
    "cancel": CancelCommand,
}

# List of one argument commands
ONE_ARG_COMMANDS = [
    "signup",
    "cancel",
]

def process_sms(phone_number, message_body):
    """Processes the incoming text and executes the related commands on the database."""
    message_body_list = message_body.strip().lower().split()
    if not message_body:
        return "Empty Message Body"
    
    command_keyword = message_body_list[0] #Command keyword == *signup* cherry, triggers what function is executed
    command_args = message_body_list[1:] # Command_args == signup *cherry*, provides arguments for specific function

    command_name = commands.get(command_keyword)

    if command_name:
        try:
            if command_keyword in ONE_ARG_COMMANDS: # Use the list of keywords
        
                if not command_args:# Check if the user actually provided an argument
                    return f"The '{command_keyword}' command requires an event code."
        
                command_instance = command_name(phone_number, command_args[0]) # Create the command instance (works for signup, cancel, etc.)
                return command_instance.execute()
    
                # Add other 'elif' blocks here for commands with different argument numbers here!
        
            else:
                # This case is for commands that are in the dictionary but not in a group
                return "Command not configured correctly."
        
        except Exception as e:
            print(f"Error in process_sms: {e}")
            return "An error occurred processing your request."
    else:
        return f"Unknown command: {command_keyword}."