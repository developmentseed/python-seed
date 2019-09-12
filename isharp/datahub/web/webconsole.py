from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool
from flask import Flask, render_template
import socket
hostname=socket.gethostname()

app = Flask(__name__)


@app.route('/')
def listing():
    print("hello world")
    listings = []
    with BrokerConnectionPool() as broker:
        for thisItem in broker.list('localhost:5672'):
            listings.append(thisItem)


    return render_template('isharp.html',hostname=hostname, my_list=listings)


