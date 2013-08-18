import subprocess
import re

# Run the DHT program to get the humidity and temperature readings!
    
output = subprocess.check_output(["./Adafruit_DHT", "11", "4"]);
print output
matches = re.search("Temp =\s+([0-9.]+)", output)

temp = float(matches.group(1))
    
# search for humidity printout
matches = re.search("Hum =\s+([0-9.]+)", output)

humidity = float(matches.group(1))
    
print "Temperature: %.1f C" % temp
print "Humidity:    %.1f %%" % humidity