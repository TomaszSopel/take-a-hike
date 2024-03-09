# TODO 1: Import Dependencies
from flask import Flask, request, jsonify

# TODO 2: Create Flask Application
app = Flask(__name__)

# TODO 5: Create a decorator 
@app.route("/")
# TODO 4: Create a Root (an endpoint on the API that we can go to to get some kind of data)
def hello_world():
    return "Hello World!"

# TODO 3: Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
