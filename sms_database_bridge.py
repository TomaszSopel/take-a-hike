import event_db, admin

class SignupCommand:
    """Handles the signup command."""
    def __init__(self, phone_number, event_code):
        self.phone_number = phone_number
        self.event_code = event_code[0] if event_code else None

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
        self.event_code = event_code[0] if event_code else None

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


class AddAdminCommand:
    """Handles the add admin command."""
    def __init__(self, phone_number, args_list):
        self.requesting_phone_number = phone_number
        self.target_phone_number = args_list[0] if args_list else None
        
    def execute(self):
        """Executes the add admin command, which is only accessible by other admins, promoting a user to admin."""
        try:
            if not admin.check_admin(self.requesting_phone_number):
                return "Operation Failed: You are not authorized to perform this action."
            
            if not self.target_phone_number:
                return "Operation Failed: Command must be structured as: add admin [target_phone_number]"


            event_db.log_user(self.target_phone_number)
            set_admin_return = admin.set_admin_status(self.target_phone_number, True)

            if set_admin_return:
                return f"Success! {self.target_phone_number} has been granted admin privileges!"
            else:
                return f"Error: Could not find or update user {self.target_phone_number}"
            
        except Exception as error:
            print(f"Error in AddAdminCommand.execute: {error}")
            return "An error occured while trying to assign a new admin."

class HeadCountCommand:
    """Executes the get_headcount admin command."""
    def __init__(self, phone_number, args_list):
        self.phone_number = phone_number
        self.event_code = args_list[0] if args_list else None

    def execute(self):
        if not admin.check_admin(self.phone_number):
            return "Access Denied. This command is for admins only."
        
        if not self.event_code:
            return "Usage Error: headcount [event code]"

        event = event_db.get_event_by_code(self.event_code)

        if not event:
            return f"Event '{self.event_code}' not found."
        
        count = admin.get_headcount(self.event_code)

        return f"There are {count} signups for {event['event_name']}"

# Dictionary of all commands
commands = {
    "signup": SignupCommand,
    "cancel": CancelCommand,
    "add admin": AddAdminCommand,
}

# List of one argument commands
ONE_ARG_COMMANDS = [
    "signup",
    "cancel",
    "add admin",
]

def process_sms(phone_number, message_body):
    """Processes the incoming text and executes the related commands on the database."""
    message_body_list = message_body.strip().lower().split()
    if not message_body:
        return "Empty Message Body"
    
    command_keyword = message_body_list[0] #Command keyword == *signup* cherry, triggers what function is executed

    if command_keyword == "add" and len(message_body_list) > 1 and message_body_list[1] == "admin":
        command_keyword = "add admin"
        message_body_list = [command_keyword] + message_body_list[2:]
    
    command_args = message_body_list[1:] # Command_args == signup *cherry*, provides arguments for specific function

    command_name = commands.get(command_keyword)
    
    if command_name:
        try:
            if command_keyword in ONE_ARG_COMMANDS: # Use the list of keywords
        
                if not command_args:# Check if the user actually provided an argument
                    return f"The '{command_keyword}' command requires an event code."
        
                command_instance = command_name(phone_number, command_args) # Create the command instance (works for signup, cancel, etc.)
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