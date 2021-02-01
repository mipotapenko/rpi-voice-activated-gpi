# Use RPI GPIO pins to blink LEDs with voice activation

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json
import led_control
from enum import IntEnum

class LEDColor(IntEnum):
	RED = 11
	GREEN = 12
	BLUE = 13
	YELLOW = 15
	WHITE = 16

def initialize_vosk(model_path, framerate, log_level):

	SetLogLevel(log_level)
	if not os.path.exists(model_path):
		print ("Please download the model from https://alphacephei.com/vosk/models and unpack to desired location.")
		exit (1)
	else:
		print("model at " + model_path + " found succesfully") 

	model = Model(model_path)
	rec = KaldiRecognizer(model, 
						  framerate, 
						  '["red", "green", "blue", "yellow", "white", "[unk]"]')
	return rec


def initialize_sound(file_path):
	wf = wave.open(file_path, "rb")
	if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
		print ("Audio file must be WAV format mono PCM.")
		exit (1)
	return wf

#This function checks a result word to see if a particular color was mentioned
def check_color(result):
	spoken_colors = {}
	if "result" in result:
		colors = ["red", "green", "blue", "yellow", "white"]
		spoken_colors = [r for r in result["result"] if r["word"] in colors]

	return spoken_colors

def channels_from_colors(colors):
	color_dict = {"red": LEDColor.RED, "green": LEDColor.GREEN, 
				  "blue": LEDColor.BLUE, "yellow": LEDColor.YELLOW, "white": LEDColor.WHITE}
	return [color_dict[color["word"]] for color in colors]


wf = initialize_sound(sys.argv[2])
rec = initialize_vosk(sys.argv[1], wf.getframerate(), 0)

with open('full_result.json', 'w') as full_result_file, open('partial_result.json', 'w') as partial_result_file:
	while True:
		data = wf.readframes(4000)
		if len(data) == 0:
		    break
		if rec.AcceptWaveform(data):
			result = rec.Result()
			full_result_file.write(result)
			spoken_colors = check_color(json.loads(result))
			channels = channels_from_colors(spoken_colors)
			led_control.blink_led(channels, 1, 0, 1)
		else:
		    partial_result_file.write(rec.PartialResult())

	result = rec.FinalResult()
	full_result_file.write(result)
	check_color(json.loads(result))
