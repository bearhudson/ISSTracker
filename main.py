import urllib.request
import requests
import json
import geopy.distance
from datetime import datetime
from turtle import Turtle, Screen
import time


class ISSTracker:

    def __init__(self):
        self.req = urllib.request.Request("http://api.open-notify.org/iss-now.json")
        self.response = urllib.request.urlopen(self.req)
        self.obj = json.loads(self.response.read())
        self.timestamp = self.obj['timestamp']
        self.latitude = self.obj['iss_position']['latitude']
        self.longitude = self.obj['iss_position']['longitude']

    def get_position(self):
        return self.latitude, self.longitude

    def set_user_position(self):
        req = requests.get("http://ipinfo.io/json")
        req.raise_for_status()
        data = req.json()
        self.user_location = data['loc']

    def get_user_position(self):
        return eval(self.user_location)

    def get_sunrise(self):
        parameters = {
            "lat": format(self.get_user_position()[0]),
            "lon": format(self.get_user_position()[1]),
            'formatted': 0,
        }
        request = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        request.raise_for_status()
        obj = request.json()
        return obj['results']['sunrise']

    def update_position(self):
        self.__init__()


screen = Screen()
screen.title("ISS Tracker")
screen.setup(height=450, width=900)
screen.bgpic("world_map.png")
time_now = datetime.now()
iss = ISSTracker()
iss.set_user_position()
iss_turtle = Turtle()
iss_turtle.color("red")
iss_turtle.penup()
home_turtle = Turtle()
home_turtle.color('green')
home_turtle.shape('circle')
home_turtle.penup()
home_x = int(float(iss.get_user_position()[1])) * 2.5
home_y = int(float(iss.get_user_position()[0])) * 2.5
print(home_x, home_y)
home_turtle.goto(x=home_x, y=home_y)


in_app = True
while in_app:
    iss_lat = format(iss.get_position()[0])
    iss_long = format(iss.get_position()[1])
    x = int(float(iss_long)) * 2.5
    y = int(float(iss_lat)) * 2.5
    iss_turtle.goto(x=x, y=y)
    iss_turtle.pendown()
    current_distance = round(geopy.distance.distance(iss.get_position(), iss.get_user_position()).miles, 1)
    print(f"Latitude: {iss_lat}\tLongitude: {iss_long} at "
          f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Distance Away:\t{current_distance} miles")
    sunrise_hour = iss.get_sunrise().split("T")[1].split(":")[0]
    sunrise_day = iss.get_sunrise().split("T")[0].split('-')[2]
    if int(sunrise_hour) < time_now.hour and int(sunrise_day) > time_now.day:
        if current_distance < 100:
            print(f"You can probably spot the ISS soon!!")
    time.sleep(60)
    iss.update_position()

screen.exitonclick()
