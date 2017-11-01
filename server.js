const WebSocket = require('ws');
const record = require('node-record-lpcm16');

// Imports the Google Cloud client library
const Speech = require('@google-cloud/speech');

// Instantiates a client
const speech = Speech();

// The encoding of the audio file, e.g. 'LINEAR16'
const encoding = 'LINEAR16';

// The sample rate of the audio file in hertz, e.g. 16000
const sampleRateHertz = 44100;

// The BCP-47 language code to use, e.g. 'en-US'
const languageCode = 'en-US';

const request = {
	config: {
		encoding: encoding,
		sampleRateHertz: sampleRateHertz,
		languageCode: languageCode
	},
	interimResults: true // If you want interim results, set this to true
};


const wss = new WebSocket.Server({
	port: 5000
});

wss.on('connection', function connection(ws) {
	// Create a recognize stream
	let recognizeStream;
	initStream();


	ws.on('message', function incoming(message) {
		recognizeStream.write(message);
	});

	function initStream() {
		recognizeStream = speech.streamingRecognize(request)
			.on('error', (err) => {
				console.log(err);
				console.log("Starting new stream")
				initStream();
			})
			.on('data', (data) => {
				ws.send(JSON.stringify(data.results));
				process.stdout.write(
					(data.results[0] && data.results[0].alternatives[0]) ?
					`Transcription: ${data.results[0].alternatives[0].transcript}\n` :
					`\n\nReached transcription time limit, press Ctrl+C\n`);
			});
				
	}
});