import os
from sms import Sms

TWILIO_SID = os.environ['TWILIO_SID'] 
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

def main():
    texter = Sms(TWILIO_SID,TWILIO_AUTH_TOKEN)
    texter.send_message("howdy")

if __name__ == "__main__":
    main()
