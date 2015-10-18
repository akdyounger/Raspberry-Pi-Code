import time
import os
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DEBUG = 0

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)
    
    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low
    
    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
    
    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1
    
    GPIO.output(cspin, True)
    
    adcout /= 2       # first bit is 'null' so drop it
    return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


# temperature sensor connected channel 0 of mcp3008
adcnum = 0
adclight = 1
waterlevel = 2



#while True:
# read the analog pin (temperature sensor LM35)
read_adc0 = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
#convert TMP36 #1 digital reading to Celsius temperature
c_temp0 = (((read_adc0 * ( 3300.0 / 1024.0)) - 100.0) / 10.0) - 40.0
c_temp0 = "%.1f" % c_temp0


read_adc1 = readadc(adclight, SPICLK, SPIMOSI, SPIMISO, SPICS)

read_adc2 = readadc(waterlevel, SPICLK, SPIMOSI, SPIMISO, SPICS)



print 'Temp:', c_temp0, 'C'
print 'Light level:', read_adc1
print
print 'ADC values:' # prints raw values
print 'Pin 1:', read_adc0
print 'Pin 2:', read_adc1
print 'Pin 3:', read_adc2



if read_adc1 in range(0, 100):
    print "Time to turn on the lights!" # dark
