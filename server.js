const WebSocket = require('ws');
const url = require('url');

// Imports the Google Cloud client library
const Speech = require('@google-cloud/speech');

// Instantiates a client
const speech = Speech();

// The encoding of the audio file, e.g. 'LINEAR16'
const encoding = 'LINEAR16';

// The sample rate of the audio file in hertz, e.g. 16000


// The BCP-47 language code to use, e.g. 'en-US'
const languageCode = 'en-US';




const wss = new WebSocket.Server({
	port: process.env.PORT
});

wss.on('connection', function connection(ws, req) {
	// Create a recognize stream
	let rt = url.parse(req.url, true).query.sampRate;
	if(rt === undefined){
		process.stdout.write(`Denied connection to ${req.url}\n`);
		ws.close();
		return;
	}
	process.stdout.write(`Accepted connection to ${req.url}\n`);
	const sampleRateHertz = parseInt(rt);

	const request = {
		config: {
			encoding: encoding,
			sampleRateHertz: sampleRateHertz,
			languageCode: languageCode
		},
		interimResults: true // If you want interim results, set this to true
	};

	let recognizeStream;
	initStream();


	ws.on('message', function incoming(message) {
		recognizeStream.write(message);
	});

	ws.on('close', function (code, reason) {
		process.stdout.write("Client connection closed\n");
	});

	ws.on('error', function (e) {
		process.stdout.write(`Socket error:\n${e}\n`);
		ws.terminate();
	});

	function initStream() {
		recognizeStream = speech.streamingRecognize(request)
			.on('error', (err) => {
				console.log(err);
				console.log("Starting new stream\n")
				initStream();
			})
			.on('data', (data) => {
				try{
					ws.send(JSON.stringify(data.results));	
				}catch(e){
					process.stdout.write("Client send error\n");
					if(ws.isAlive === false) ws.terminate();
				}
			});
	}
});