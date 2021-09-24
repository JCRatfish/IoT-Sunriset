from astral import *
from astral.sun import *
from datetime import *
from pytz import timezone
import datetime, pytz, sys, time
import RPi.GPIO as GPIO

# Setup runtime parameters
city = LocationInfo("Toronto", "Ontario", "America/Toronto", 43.754543, -79.361615)
lights = True
output_pin = 12
prevResult = None
toronto = timezone("America/Toronto")

# Initialize Raspberry Pi GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(output_pin, GPIO.OUT)

# Main loop
while True:
	# All times used for calculations should be UTC
	utcdatetime = datetime.datetime.now(datetime.timezone.utc)
	utctoday = datetime.datetime.strptime(utcdatetime.strftime("%Y-%m-%d"), "%Y-%m-%d")
	s = sun(city.observer, date=utctoday)

	# Set the lights variable to control the GPIO
	if utcdatetime < s["sunrise"] and utcdatetime < s["sunset"]:
		# Before sunrise and sunset: OFF
		lights = False
	elif utcdatetime > s["sunrise"] and utcdatetime > s["sunset"]:
		# After sunrise and sunset: OFF
		lights = False
	elif utcdatetime > s["sunrise"] and utcdatetime < s["sunset"]:
		# After sunrise and before sunset: ON
		lights = True
	elif utcdatetime < s["sunrise"] or utcdatetime > s["sunset"]:
		# Before sunrise or after sunset: OFF
		lights = False

	# Output to the GPIO if the lights variable differs from the prevResult variable
	if prevResult != lights:
		prevResult = lights

		# Set the GPIO output
		GPIO.output(output_pin, GPIO.HIGH) if lights else GPIO.output(output_pin, GPIO.LOW)

		# Log -- MUST output to a file or the system will crash!!
		with open('/home/pi/sunriset.log', 'a') as log:
			# Change the standard output to the file we created.
			sys.stdout = log
			print ("Lights: ON") if lights else print ("Lights: OFF")
			print((
				f"Date:     {toronto.localize(datetime.datetime.now())}\n"
				f"DateUTC:  {utcdatetime}\n"
				f"Sunrise:  {s['sunrise']}\n"
				f"Sunset:   {s['sunset']}\n"
			))

		# Close the file
		log.close()

	# Loop every minute
	time.sleep(60)
