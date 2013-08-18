import RPi.GPIO as GPIO
import time

# blink(pin) is andrew's first python routine.
def blink(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.1)
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.2)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.2)
	
def dot(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.1)

def dash(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.4)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.4)
	
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)

for i in range (0, 10):
	#blink(11)
	dash(11)
	dash(11)
	dash(11)
	
	dot(11)
	dot(11)
	dot(11)
	time.sleep(0.3)
	
	dash(11)
	dash(11)
	dash(11)
	time.sleep(1)
	
GPIO.cleanup()
