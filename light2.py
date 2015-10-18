import RPi.GPIO as GPIO
import time

# Tell the GPIO library to use
# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)

# Define function to measure charge time
def RCtime (PiPin):
    measurement = 0
    # Discharge capacitor
    GPIO.setup(PiPin, GPIO.OUT)
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(0.01)


    GPIO.setup(PiPin, GPIO.IN)
    # Count loops until voltage across
    # capacitor reads high on GPIO
    while (GPIO.input(PiPin) == GPIO.LOW):
        measurement += 1

    return measurement


listOfMeasurements = [] # this is an empty list of numbers (well, empty list of anythings)

for i in range (0, 100):
    listOfMeasurements.append(RCtime(18))

# now we have a list of 100 numbers.
sumOfList = sum(listOfMeasurements)
lengthOflist = len(listOfMeasurements)
meanOfList = sum(listOfMeasurements)/(len(listOfMeasurements)*1.0) # * 1.0 forces a floating point division
maximumInList = max(listOfMeasurements)
minimumInList = min(listOfMeasurements)


print "Mean:",meanOfList
print "Maximum:",maximumInList
print "Minimum:",minimumInList

#Adding in some qualitative values to make sense of the numbers
if maximumInList in range(3000, 4000):
    print "Light level: Dim"
if maximumInList in range(0, 3000):
    print "Light level: Dark"



# And that's the sum total of the statistics I can code off the top of my head.
# you should look into downloading and using the NUMPY package - google numpy python

# Main program loop
#while True:
#    print RCtime(7) # Measure timing using GPIO4


GPIO.cleanup()