import datetime
import os
from turtle import Screen
from iss import ISSTracker
from home_location import HomeLocation
import email_notifier
import time
import geopy.distance

EMAIL = os.environ.get('EMAIL')
PASS = os.environ.get('PASS')
SERVER = os.environ.get('SERVER')
FROM = os.environ.get('FROM')

screen = Screen()
screen.title("PySS Tracker")
screen.setup(height=450, width=900)
screen.bgpic("map.png")
iss = ISSTracker()
home = HomeLocation()

old_x = iss.x
is_tracking = True

while is_tracking:
    iss.update_position()
    iss.set_grid_position()
    distance = round(geopy.distance.distance(iss.get_gps(), home.get_gps()).miles, 1)
    print(f"{time.strftime('%H:%M:%S %Z')}-> The ISS is: {distance} miles away.")
    if distance < 50 and not home.check_daylight():
        email_notifier.send_message(iss.get_gps(), distance)
    if iss.x < old_x:
        iss.penup()
        iss.move()
        iss.penup()
    else:
        iss.move()
        iss.pendown()
    old_x = iss.x
    time.sleep(15)

screen.exitonclick()
