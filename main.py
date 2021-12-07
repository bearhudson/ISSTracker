import os
from turtle import Screen
from iss import ISSTracker
from home_location import HomeLocation
import email_notifier
import time
import geopy.distance

EMAIL = os.environ.get('EMAIL')
PASS = os.environ.get('MY_PASS')
SERVER = os.environ.get('MY_SERVER')
FROM = os.environ.get('MY_FROM')

screen = Screen()
screen.title("ISS Tracker")
screen.setup(height=450, width=900)
# screen.bgpic("world_map.png")
screen.bgpic("new_map.png")
iss = ISSTracker()
home = HomeLocation()

old_x = iss.x
is_tracking = True

while is_tracking:
    iss.update_position()
    iss.set_grid_position()
    distance = round(geopy.distance.distance(iss.get_gps(), home.get_gps()).miles, 1)
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
    time.sleep(5)

screen.exitonclick()
