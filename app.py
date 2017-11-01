from flask import Flask
from flask_sockets import Sockets
import random
import json

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

class SpeechToTextWS(object):

	def __init__(self, ws):
		self._ws = ws
		self._client = speech.SpeechClient()
		self._config = types.RecognitionConfig( encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=RATE, language_code='en-US', enable_word_time_offsets=1)
		self._sconfig = types.StreamingRecognitionConfig( config=self._config, interim_results=False)

	def generator(self):
		while not self._ws.closed:
			chunk = str.encode(self._ws.receive().encode('ascii','replace'))
			data = [chunk]
			yield b''.join(data)

	def recog_loop(self):
		generator = self.generator()
		res = self._client.streaming_recognize(self._sconfig, (types.StreamingRecognizeRequest(audio_content=content) for content in generator))
		for response in res:
			if not response.results:
				continue

			result = response.results[0]
			if not result.alternatives:
				continue

			transcript = result.alternatives[0].transcript

			ws.send(transcript)


@sockets.route('/echo')
def echo_socket(ws):
	stt = SpeechToTextWS(ws)
	stt.recog_loop()
		


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()