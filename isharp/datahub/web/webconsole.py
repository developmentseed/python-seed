from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello_world():
    listings = []
    with BrokerConnectionPool() as broker:
        for thisItem in broker.list('localhost:5672'):
            listings.append(thisItem)


    return render_template('isharp.html',my_string="Wheeeee!", my_list=listings)


