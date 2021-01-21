#!/usr/bin/env python3

#[model path][wavefile path]

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave

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
rec = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(44100)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())
