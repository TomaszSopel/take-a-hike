# TODO 1: Import Dependencies
from flask import Flask, request, jsonify
from sms import Sms
import logging


# TODO 2: Create Flask Application
app = Flask(__name__)

# TODO 5: Create a decorator 
@app.route("/", methods = ['GET'])
# TODO 4: Create a Root (an endpoint on the API that we can go to to get some kind of data)
def hello_world():
    messenger = Sms()
    messenger.send_message("Get Message Sent")
    logging.info("Hello world started")
    return "Hello World! World!"

@app.route('/', methods=['POST'])
def receive_text():
    if request.method == 'POST':
        message_body = request.get_json()
        print(message_body)

# TODO 3: Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
