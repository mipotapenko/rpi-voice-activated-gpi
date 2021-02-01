# Basic LED control functions
# Uses physical board numberings

import RPi.GPIO as GPIO
import time
import sys
from enum import IntEnum


class errors(IntEnum):
	NEG_DUR = 8
	NEG_GAP = 4
	NEG_BLINKS = 2
	OTHER = 1
# negative duration 1000
# negative gap 0100
# negative blinks 0010
# other 0001

def blink_led(channels, duration_s, gap_s, blinks_n):

	error = 0;
	if duration_s < 0:
		print("Error: negative duration requested")
		error = error | errors.NEG_DUR
	if gap_s < 0: 			
		print("Error: requested gap is negative.")
		error = error | errors.NEG_GAP
	if blinks_n < 0:
		print("Error: requested number of blinks is negative.")
		error = error | errors.NEG_BLINKS

	if error == 0 and duration_s > 0 and blinks_n > 0:
		try:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(channels, GPIO.OUT)
				
			for i in range(blinks_n):	
				GPIO.output(channels, GPIO.HIGH)
				time.sleep(duration_s)
				GPIO.output(channels, GPIO.LOW)
				if i != blinks_n - 1:
					time.sleep(gap_s)

		except:
			print(sys.exc_info())
			error = error | errors.OTHER

		finally:
			GPIO.cleanup(channels)
	
	return error


