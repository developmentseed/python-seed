import websocket
import threading
import time
import json
import pika
from datetime import datetime, timezone,timedelta

start_millis = int(round(time.time() * 1000))
msg_key = start_millis
connection = pika.BlockingConnection(pika.ConnectionParameters(host='daphne174'))
offset =  timezone(timedelta(hours=0))
format = "%Y-%m-%dT%H:%M:%S.%f %Z"


def on_message(ws, message):
    now = datetime.now(offset)
    props = pika.BasicProperties(

                                 app_id="polozilla",
                                 type="classic",
                                 user_id="guest",
                                 content_encoding="UTF-16",
                                 content_type="application/octet",
                                 delivery_mode=2,
                                 expiration="60000",
                                 headers=[],
                                 priority=1,
                                 reply_to="n/a"

    )

    if (message!='[1002,1]'):
      msg_with_timestamp =   '{}{}'.format(now.strftime(format), message)
      print(msg_with_timestamp)
      channel.basic_publish(exchange='', routing_key="pol.tickers", body=msg_with_timestamp,properties=props)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closing connection ###")
    connection.close()
    print("### closed ###")

def on_open(ws):
    print("ONOPEN")
    def run(*args):
        # ws.send(json.dumps({'command':'subscribe','channel':1001}))
        ws.send(json.dumps({'command':'subscribe','channel':1002}))
        # ws.send(json.dumps({'command':'subscribe','channel':1003}))
        # ws.send(json.dumps({'command':'subscribe','channel':1010}))
        # ws.send(json.dumps({'command':'subscribe','channel':'BTC_XMR'}))
        time.sleep(1800)
        ws.close()
        print("thread terminating...")
    threading.Thread(target = run).start()


if __name__ == "__main__":

    channel = connection.channel()
    channel.queue_declare("pol.tickers", durable=False)

    ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()


