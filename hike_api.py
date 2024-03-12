# TODO 1: Import Dependencies
import logging
from flask import Flask, request
from sms import Sms


handler = logging.FileHandler('hike_api.log')
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

@app.route('/', methods = ['POST'])
def receive_text():
    try:
        if request.method == 'POST':
            from_number = request.form.get("From")
            from_body = request.form.get("Body")
            
            messenger = Sms()
            messenger.send_message(f"Message sent from: {from_number}")
            messenger.send_message(f"Message Body: {from_body}")
            return "Message received successfully!", 200
    except Exception as e:
        logging.error(f"Error Message: {e}")
        return "Error occurred", 500
# TODO 3: Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
