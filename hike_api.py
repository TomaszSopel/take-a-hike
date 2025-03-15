import logging, event_db, sms_database_bridge
from flask import Flask, request
from sms import Sms

app = Flask(__name__)

@app.route("/", methods = ['GET'])

def hello_world():
    phone_number = request.form.get("From") # This object uses the phone number and message body from the incoming text as arguments during initalization
    message_body = request.form.get("Body")
    messenger = Sms()
    messenger.send_sms(to_number=phone_number, body=message_body)
    logging.info("Hello world started")
    return "Hello World!"

@app.route("/database", methods = ['GET'])

def database_test():
    return event_db.get_events()

@app.route('/', methods = ['POST'])
def receive_text():
    try:
        if request.method == 'POST': # When a text comes in from Twilio, it sends a post request to the root of the API
            phone_number = request.form.get("From") # This object uses the phone number and message body from the incoming text as arguments during initalization
            message_body = request.form.get("Body")
            logging.info(f"Incoming message: From={phone_number}, Body={message_body}")

            response_message = sms_database_bridge.process_sms(phone_number, message_body)
            message = Sms()
            message.send_sms(to_number=phone_number, body=response_message)
            return "Message received successfully!", 200
    except Exception as e:
        logging.error(f"Error Message: {e}")
        return "Error occurred", 500

if __name__ == "__main__":
    app.run(debug=True)


"""
Test curl command: 

curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/x-www-form-urlencoded" -d "Body=Signup Cherry" -d "From=18609673158"

"""