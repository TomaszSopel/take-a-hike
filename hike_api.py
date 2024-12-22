import os
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
        if request.method == 'POST':
            incoming_message = sms_database_bridge.Text_message_input(
                phone_number=request.form.get("From"),
                body=request.form.get("Body"))
            incoming_message.process_text()
            return "Message received successfully!", 200
    except Exception as e:
        logging.error(f"Error Message: {e}")
        return "Error occurred", 500
# #Function testing receiving a text
# def test_receive_text():
#     with app.test_client() as client:
#         mock_data = {
#             "From": "+8601234567",
#             "Body": "Signup Cherry"
#         }

#         response = client.post('/', data=mock_data)
        
#         print("Response status:", response.status_code)
#         print("Response data:", response.data.decode())

# test_receive_text()
if __name__ == "__main__":
    app.run(debug=True)
