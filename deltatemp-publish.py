import time
import os
import RPi.GPIO as GPIO
import subprocess
import re
import tweepy
import datetime
import math
import sys


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
adct1 = 0
adct2 = 1
adcl1 = 2



#while True:
# read the analog pin (temperature sensor LM35)
read_adc0 = readadc(adct1, SPICLK, SPIMOSI, SPIMISO, SPICS)
read_adc1 = readadc(adct2, SPICLK, SPIMOSI, SPIMISO, SPICS)
read_adc2 = readadc(adcl1, SPICLK, SPIMOSI, SPIMISO, SPICS)

#convert TMP36 #1 digital reading to Celsius temperature
c_temp0 = (((read_adc0 * ( 3300.0 / 1024.0)) - 100.0) / 10.0) - 40.0
#c_temp0 = "%.1f" % c_temp0
c_temp1 = (((read_adc1 * ( 3300.0 / 1024.0)) - 100.0) / 10.0) - 40.0
#c_temp1 = "%.1f" % c_temp1

f_temp0 = ((c_temp0 * (9.0/5.0)) + 32.0)
f_temp1 = ((c_temp1 * (9.0/5.0)) + 32.0)

#raw values
f_tempreal0 = "%.1F" % f_temp0
f_tempreal1 = "%.1F" % f_temp1

#for delta calculations
delta = f_temp1 - f_temp0


if -2 <= delta <= 2:
    deltatweet = 'The greenhouse is about the same temperature as outside, at'
elif delta < 2:
    deltatweet = 'The greenhouse is keeping the environment colder than outside, at'
elif -2 < delta:
    deltatweet = 'The greenhouse is keeping the environment warmer than outside, at'




light = ((read_adc2/1024.0) * 100)
light = "%.1F" % light


print 'Temp1:', f_tempreal0, 'F'
print 'Temp2:', f_tempreal1, 'F'
print 'Light percentage:', light
print
print 'ADC values:'
print 'Pin 1:', read_adc0
print 'Pin 2:', read_adc1
print 'Pin 3:', read_adc2



#Twiiter Parts
CONSUMER_KEY = '###'
CONSUMER_SECRET = '###'
ACCESS_KEY = '###'
ACCESS_SECRET = '###'

devicename = "Pi Farm" # make yours different, say, "Pi"
## Setup today
today = datetime.datetime.now()

# gets core temperature info
cmd = '/opt/vc/bin/vcgencmd measure_temp'
line = os.popen(cmd).readline().strip()
coretemp = line.split('=')[1].split("'")[0]

# converts the coretemp to F
coretempf = float(coretemp) * (9.0/5.0) + 32.0

# access twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


#The Tweets!
#Diagnostic tweet
#TweetStatus = "%s [%s.%s] CPU: %s F. Room: %s F. Greenhouse is %s F. Light level is %s %% of max. " % (devicename, today.minute, today.second, coretempf, f_tempreal0, f_tempreal1, light)


#More complex tweet
TweetStatus = "%s [%s.%s] CPU: %s F. %s %s F. Light level is %s %% of max. " % (devicename, today.minute, today.second, coretempf, deltatweet, f_tempreal1, light)

status = TweetStatus


try:
    api.update_status(status = TweetStatus)
except tweepy.error.TweepError as e :
    print status
    print "Error from Tweepy:", e
