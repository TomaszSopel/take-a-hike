# TODO 1: Import Dependencies
import os
import logging, event_db, sms_database_bridge
from flask import Flask, request
from sms import Sms



# TODO 2: Create Flask Application
app = Flask(__name__)

# TODO 5: Create a decorator 
@app.route("/", methods = ['GET'])
# TODO 4: Create a Root (an endpoint on the API that we can go to to get some kind of data)
def hello_world():
    messenger = Sms()
    messenger.send_message("Get Message Sent")
    logging.info("Hello world started")
    return "Hello World!"

@app.route("/database", methods = ['GET'])
# TODO 4: Create a Root (an endpoint on the API that we can go to to get some kind of data)
def database_test():
    return event_db.get_events()

@app.route('/', methods = ['POST'])
def receive_text():
    try:
        if request.method == 'POST':
            incoming_message = sms_database_bridge.Text_message_input(
                phone_number=request.form.get("From"),
                body=request.form.get("Body"))
            incoming_message.process_text()
            
            return "Message received successfully!", 200
    except Exception as e:
        logging.error(f"Error Message: {e}")
        return "Error occurred", 500
# TODO 3: Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
