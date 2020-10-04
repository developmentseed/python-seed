import websocket
import threading
import time
import json
from datetime import datetime
start_millis = int(round(time.time() * 1000))
msg_key = start_millis
mst = str(datetime.now().microsecond)

def on_message(ws, message):
    print (message)



def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closing connection ###")
    #connection.close()
    print("### closed ###")

def on_open(ws):
    print("ONOPEN")
    def run(*args):
        # ws.send(json.dumps({'command':'subscribe','channel':1001}))
        ws.send(json.dumps({'command':'subscribe','channel':1002}))
        # ws.send(json.dumps({'command':'subscribe','channel':1003}))
        # ws.send(json.dumps({'command':'subscribe','channel':1010}))
        # ws.send(json.dumps({'command':'subscribe','channel':'BTC_XMR'}))
        time.sleep(15)
        ws.close()
        print("thread terminating...")
    threading.Thread(target = run).start()


if __name__ == "__main__":


    ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()