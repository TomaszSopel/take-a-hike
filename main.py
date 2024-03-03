import os
from sms import Sms
from twilio.rest import Client

TWILIO_SID = os.environ['TWILIO_SID'] 
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

def main():
    # texter = Sms(TWILIO_SID,TWILIO_AUTH_TOKEN)
    # texter.send_message("howdy")

    # client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     from_ = "+18337970829",
    #     to = "+18609679255",        
    #     body = "Testing!"
    # )
    # print(message.sid)

    messenger = Sms(TWILIO_SID,TWILIO_AUTH_TOKEN)
    messenger.send_message("Message sent Via Sms.py Class!")
    

if __name__ == "__main__":
    main()
