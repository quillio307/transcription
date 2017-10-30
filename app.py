from flask import Flask
from flask_sockets import Sockets
import random

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
	rand = random.randrange(100)
	while not ws.closed:
		message = ws.receive()
		print(message)
		ws.send("This is my random number: " + str(rand))


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()