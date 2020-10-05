from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool

from flask import Flask, render_template
import os
import socket

import json
hostname=socket.gethostname()
from flask import request

templates_dir =  os.getenv('isharp_web_templates', 'templates')
static_dir = os.getenv('isharp_web_static', '/isharp-core/docs')

tableContent = [

    [   "plant/plough.gif"
        ,"plant/seed_and_sprout.gif"
        ,"plant/seed_sprouting.gif"
        ,"plant/sunny_sprout.gif"
        ,"plant/seeding_trailer.gif"
        ,"plant/wheat_seedling.gif"
    ]

    ,[  "feed/raindrops.gif"
        ,"feed/irrigation_pipe.gif"
        ,"feed/airplane_irrigation.gif"
        ,"feed/raindrop_with_cog.gif"
        ,"feed/feed_spreader.gif"
        ,"feed/raindrops.gif"


    ]

    ,["develop/measure_height.gif"
        ,"develop/seed_lab.gif"
        ,"develop/seed_time.gif"
        ,"develop/chemicals.gif"
        ,"develop/measure_height.gif"
        ,"develop/hay_bail.gif"

    ]


    ,["harvest/combine_harvester.gif"
        ,"harvest/bailing_tractor.gif"
        ,"harvest/grain_silo.gif"
        ,"harvest/thresher_trailer.gif"
        ,"harvest/mini_harvester.gif"
        ,"harvest/distillery.gif"

    ]


]

print ("templates_dir: {}".format(templates_dir))
print ("static_dir: {}  ? {}".format(static_dir,os.path.exists(static_dir)))

app = Flask(__name__,template_folder=templates_dir, static_folder=static_dir)
app.config["CACHE_TYPE"] = 'null'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

hub_host =  os.getenv('isharp_hub_host', 'localhost:5672')
isharp_dev_hostname =  os.getenv('isharp_dev_hostname', 'isharpdev')

@app.route('/')
def static_content():

    return render_template("index.html",table_images = tableContent, isharp_hostname=isharp_dev_hostname)

@app.route('/datahub')
def listing():
    brokers = [["Demo Broker","Prod parallel demo broker"],["UAT","UAT broker"],["DEV","Dev broker"]]
    listings = []
    with BrokerConnectionPool() as broker:
        for thisItem in broker.list(hub_host):
            listings.append(thisItem)
    return render_template('datahub_index.html',hostname="rabbit", my_list=listings,hub_host="Demo  Data Broker", brokers=brokers)


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

