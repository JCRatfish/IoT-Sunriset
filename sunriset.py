from astral import *
from astral.sun import *
from datetime import timedelta, datetime
import datetime
import time
import pytz
import RPi.GPIO as GPIO

now = datetime.datetime.now(datetime.timezone.utc)
todayutc = datetime.datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
city = LocationInfo("Toronto", "Ontario", "America/Toronto", 43.754543, -79.361615)
output_pin = 12
s = sun(city.observer, date=todayutc)
lights = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(output_pin, GPIO.OUT)

while True:

	now = datetime.datetime.now(datetime.timezone.utc)
	todayutc = datetime.datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")

	if now < s["sunrise"] and now < s["sunset"]:
		s = sun(city.observer, date=todayutc - timedelta(days=1))
		lights = False
	elif now > s["sunrise"] and now < s["sunset"]:
		lights = True
	elif now > s["sunset"] or now < s["sunrise"]:
		lights = False

	if lights == True:
		print ("lights on")
		GPIO.output(output_pin, GPIO.HIGH)
	else:
		print("lights off")
		GPIO.output(output_pin, GPIO.LOW)

	print((
		f"Information for {city.name}/{city.region}\n"
		f"Date:	 {datetime.datetime.now()}\n"
		f"DateUTC:  {datetime.datetime.now(datetime.timezone.utc)}\n"
		f"Sunrise:  {s['sunrise']}\n"
		f"Sunset:   {s['sunset']}\n"
	))

	time.sleep (60)
