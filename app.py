from flask import Flask
from flask_sockets import Sockets
import random

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

app = Flask(__name__)
sockets = Sockets(app)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
TIME = 0.00

a = 5


@sockets.route('/echo')
def echo_socket(ws):
	language_code = 'en-US'  # a BCP-47 language tag
	client = speech.SpeechClient()
	config = types.RecognitionConfig( encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=RATE, language_code=language_code, enable_word_time_offsets=1)
	streaming_config = types.StreamingRecognitionConfig( config=config, interim_results=False)
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