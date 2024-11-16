import os
from sms import Sms
from twilio.rest import Client
from hike_api import app
import logging

def main():
    logging.info("Main Started")
    

if __name__ == "__main__":
    main()
    app.run(debug=True)

print(os.environ.get("fu"))