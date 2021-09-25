from astral import *
from astral.sun import *
from datetime import *
from pyfirmata import Arduino, util
from pytz import timezone
import datetime, pytz, sys, time

# Setup variables
city = LocationInfo("Toronto", "Ontario", "America/Toronto", 43.754543, -79.361615)
output = True
output_pin = 12
output_previous_result = None
toronto = timezone("America/Toronto")

# Initialize Arduino
arduino = Arduino('COM3')

# Main loop
while True:
	# All times used for calculations should be UTC
	utcdatetime = datetime.datetime.now(datetime.timezone.utc)
	utctoday = datetime.datetime.strptime(utcdatetime.strftime("%Y-%m-%d"), "%Y-%m-%d")
	s = sun(city.observer, date=utctoday)

	# Set the output variable
	if utcdatetime < s["sunrise"] and utcdatetime < s["sunset"]:
		# Before sunrise and sunset: OFF
		output = False
	elif utcdatetime > s["sunrise"] and utcdatetime > s["sunset"]:
		# After sunrise and sunset: OFF
		output = False
	elif utcdatetime > s["sunrise"] and utcdatetime < s["sunset"]:
		# After sunrise and before sunset: ON
		output = True
	elif utcdatetime < s["sunrise"] or utcdatetime > s["sunset"]:
		# Before sunrise or after sunset: OFF
		output = False

	# Output to the Arduino if output differs from output_previous_result
	if output_previous_result != output:
		output_previous_result = output

		# Set the Arduino output
		arduino.digital[13].write(output) # Arduino LED
		arduino.digital[output_pin].write(output)

	# Loop every minute
	time.sleep(60)
