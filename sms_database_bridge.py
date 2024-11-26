import event_db
class Text_message_input:
    """Creates Text_message_input object that can send messages via Twilio API"""
    def __init__(self, phone_number, body):
        self.phone_number = phone_number
        self.body = body

    def process_text(self):
        if "signup" in self.body:
            events_list = event_db.get_events()
            print(events_list)
            


text = Text_message_input('8609999999', ["signup", "cherry"])
text.process_text()
