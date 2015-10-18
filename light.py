import RPi.GPIO as GPIO
import time

# Tell the GPIO library to use
# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)

# Define function to measure charge time

for i in range (0, 3):

    def RCtime (PiPin):
        measurement = 0
        # Discharge capacitor
        GPIO.setup(PiPin, GPIO.OUT)
        GPIO.output(PiPin, GPIO.LOW)
        time.sleep(1.0)
    
    
        GPIO.setup(PiPin, GPIO.IN)
        # Count loops until voltage across
        # capacitor reads high on GPIO
        while (GPIO.input(PiPin) == GPIO.LOW):
            measurement += 1
    
        return measurement



    # Main program loop
    while True:
        print RCtime(7) # Measure timing using GPIO4


GPIO.cleanup()