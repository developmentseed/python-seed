from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool
from flask import Flask, render_template
import os
import socket
hostname=socket.gethostname()
from flask import request
app = Flask(__name__)

hub_host =  os.getenv('isharp_hub_host', 'localhost:5672')

@app.route('/')
def listing():
    print("hello world")
    listings = []
    with BrokerConnectionPool() as broker:
        for thisItem in broker.list(hub_host):
            listings.append(thisItem)


    return render_template('index.html',hostname=hostname, my_list=listings,hub_host=hub_host)


@app.route('/datahub/view/<path:path>', methods=['GET'])
def view(path):
    databroker = BrokerConnectionPool()
    protocol = request.args.get('protocol')
    url = "{}://{}/{}".format(protocol,hub_host,path)

    m = databroker.view(url)
    return render_template('matrix.html',matrix=m)




