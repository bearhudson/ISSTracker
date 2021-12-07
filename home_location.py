import requests
from turtle import Turtle
from datetime import time, datetime

COLOR = "green"
SHAPE = "circle"


class HomeLocation(Turtle):
    def __init__(self):
        super().__init__()
        self.datetime_now = datetime.now()
        self.time = time()
        self.penup()
        self.color(COLOR)
        self.shape(SHAPE)
        self.x = 0
        self.y = 0
        req = requests.get("http://ipinfo.io/json")
        req.raise_for_status()
        data = req.json()
        self.user_location = data['loc']
        self.set_user_position()
        self.get_gps()
        self.goto(self.x, self.y)
        self.sunrise = self.get_sunrise()
        self.sunrise_hour = self.get_sunrise().split("T")[1].split(":")[0]
        self.sunrise_day = self.get_sunrise().split("T")[0].split('-')[2]

    def get_sunrise(self):
        parameters = {
            "lat": format(self.get_gps()[0]),
            "lon": format(self.get_gps()[1]),
            'formatted': 0,
        }
        request = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        request.raise_for_status()
        obj = request.json()
        return obj['results']['sunrise']

    def set_user_position(self):
        self.y = float(format(self.get_gps()[0])) * 2.5
        self.x = float(format(self.get_gps()[1])) * 2.5

    def get_gps(self):
        return eval(self.user_location)

    def check_daylight(self):
        if int(self.sunrise_hour) <= self.datetime_now.hour and int(self.sunrise_day) >= self.datetime_now.day:
            return True
        else:
            return False
