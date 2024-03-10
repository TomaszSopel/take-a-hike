import os
from sms import Sms
from twilio.rest import Client
from hike_api import app

TWILIO_SID = os.environ['TWILIO_SID'] 
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

def main():
    messenger = Sms(TWILIO_SID,TWILIO_AUTH_TOKEN)
    messenger.send_message("Test Message")
    

if __name__ == "__main__":
    main()
    app.run(debug=True)
