import logging, os, event_db, sms_database_bridge
from flask import Flask, request, Response
from sms import Sms
from twilio.rest import Client

app = Flask(__name__)

account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_NUMBER")
port = int(os.environ.get("PORT", 5000)) # Default to 5000

sms_sender = None # Initialize sms_sender to None
if account_sid and auth_token and twilio_number:
    try:
        # Create the REAL Twilio client ONCE
        twilio_client = Client(account_sid, auth_token)
        # Create the Sms object ONCE, passing the client
        sms_sender = Sms(twilio_client)
        logging.info("Twilio client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Twilio client: {e}")
else:
    logging.warning("Twilio credentials or phone number not set in environment variables.")

@app.route("/database", methods = ['GET'])

def database_test():
    return event_db.get_events()

@app.route('/', methods = ['POST'])
def receive_text():
    try:
        phone_number = request.form.get("From") # This object uses the phone number and message body from the incoming text as arguments during initalization
        message_body = request.form.get("Body")
        logging.info(f"Incoming message: From={phone_number}, Body={message_body}")

        response_message = sms_database_bridge.process_sms(phone_number, message_body)
       
        if sms_sender and response_message:
            sms_sender.send_sms(phone_number, response_message)
            return Response("OK"), 200
        else: 
            return Response("Error, message not sent"), 500
        
    except Exception as e:
        logging.error(f"Error Message: {e}")
        return "Error occurred", 500

if __name__ == "__main__":
    app.run(debug=True)


"""
Test curl command: 

curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/x-www-form-urlencoded" -d "Body=Signup Cherry" -d "From=18609673158"

"""