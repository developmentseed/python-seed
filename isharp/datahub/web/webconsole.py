from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool

from flask import Flask, render_template, jsonify
import os
import socket
import json
hostname=socket.gethostname()
from flask import request
app = Flask(__name__)

hub_host =  os.getenv('isharp_hub_host', 'localhost:5672')

@app.route('/')
def listing():
    brokers = [["Demo Broker","Prod parallel demo broker"],["UAT","UAT broker"],["DEV","Dev broker"]]
    listings = []
    with BrokerConnectionPool() as broker:
        for thisItem in broker.list(hub_host):
            listings.append(thisItem)
    return render_template('index.html',hostname="rabbit", my_list=listings,hub_host="Demo  Data Broker", brokers=brokers)


@app.route('/datahub/view/<path:path>', methods=['GET'])
def view(path):
    databroker = BrokerConnectionPool()
    protocol = request.args.get('protocol')
    url = "{}://{}/{}".format(protocol,hub_host,path)
    mtx = databroker.view(url)

    row_data = []
    dict_array = mtx.content.to_dict(orient='records')
    for idx, row in enumerate(dict_array):
        row["date"]=mtx.content.index[idx]
        row_data.append(row)

    column_headers = list(mtx.content)
    column_headers.insert(0,"date")
    history = databroker.history(url)


    return render_template('matrix.html',
                           column_headers=column_headers,
                           row_data = row_data,
                           revision_list = history)

