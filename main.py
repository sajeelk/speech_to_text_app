# TRANSCRIBING -----------
import requests, json
from requests.auth import HTTPBasicAuth
from config import config

def transcribe_from_file(filename):
	with open(filename, 'rb') as f:
		r = requests.post(config['url'] + '/v1/recognize',
			auth=('apikey', config['apikey']),
			files={filename: f},
			headers={'Content-Type': 'audio/flac'})
	return(json.loads(r.text)['results'][0]['alternatives'][0]['transcript'])

# RECORDING --------------
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf

if __name__ == '__main__':
	fs = 44100
	duration = 5 # seconds
	myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float64')
	print("Recording Audio")
	sd.wait()
	print("Audio recording complete, Play Audio")
	sd.play(myrecording, fs)
	sd.wait()
	print("Play Audio Complete")
	wav.write('out.wav', fs, myrecording)
	data, samplerate = sf.read('out.wav')
	sf.write('out.flac', data, samplerate)
	print(transcribe_from_file('out.flac'))