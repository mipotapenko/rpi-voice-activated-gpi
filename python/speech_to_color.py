#!/usr/bin/env python3

#[model path][wavefile path]

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json

#This function checks a result word to see if a particular color was mentioned
def check_color(result):
	spoken_colors = {}
	if "result" in result:
		colors = ["red", "green", "blue", "yellow", "white"]
		spoken_colors = [r for r in result["result"] if r["word"] in colors]

	return spoken_colors

SetLogLevel(0)

model_path = sys.argv[1]

if not os.path.exists(model_path):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack to desired location.")
    exit (1)
else:
	print("model at " + model_path + " found succesfully") 

wf = wave.open(sys.argv[2], "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model(model_path)
rec = KaldiRecognizer(model, wf.getframerate(), '["red", "green", "blue", "yellow", "white", "[unk]"]')

with open('full_result.json', 'w') as full_result_file, open('partial_result.json', 'w') as partial_result_file:
	while True:
		data = wf.readframes(4000)
		if len(data) == 0:
		    break
		if rec.AcceptWaveform(data):
			result = rec.Result()
			full_result_file.write(result)
			check_color(json.loads(result))
		else:
		    partial_result_file.write(rec.PartialResult())

	result = rec.FinalResult()
	full_result_file.write(result)
	check_color(json.loads(result))



