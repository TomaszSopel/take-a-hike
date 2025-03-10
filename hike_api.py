import logging, event_db, sms_database_bridge
from flask import Flask, request
from sms import Sms

app = Flask(__name__)

@app.route("/", methods = ['GET'])

def hello_world():
    messenger = Sms()
    messenger.send_message("Get Message Sent")
    logging.info("Hello world started")
    return "Hello World!"

@app.route("/database", methods = ['GET'])

def database_test():
    return event_db.get_events()

@app.route('/', methods = ['POST'])
def receive_text():
    try:
        if request.method == 'POST': # When a text comes in from Twilio, it sends a post request to the root of the API
            incoming_message = sms_database_bridge.Text_message_input( # An incoming_message object is created from the Text_message_input class.
                phone_number=request.form.get("From"), # This object uses the phone number and message body from the incoming text as arguments during initalization
                body=request.form.get("Body"))
            incoming_message.process_text() # Process_text handles how to text processing, duh.
            return "Message received successfully!", 200
    except Exception as e:
        logging.error(f"Error Message: {e}")
        return "Error occurred", 500

if __name__ == "__main__":
    app.run(debug=True)
