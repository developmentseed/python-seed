
from datetime import datetime
from flask import Flask
app = Flask(__name__)

@app.route("/motionEye")
def hello():
    print("motion "  , datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    print('\a')

    return "Hello World!"

if __name__ == "__main__":
    app.run(host='192.168.86.57')