from turtle import Turtle
import requests


class ISSTracker(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("red")
        self.x = 0
        self.y = 0
        self.update_position()
        self.set_grid_position()

    def update_position(self):
        self.req = requests.get("http://api.open-notify.org/iss-now.json")
        self.req.raise_for_status()
        self.req_json = self.req.json()
        self.timestamp = self.req_json['timestamp']
        self.iss_lat = self.req_json['iss_position']['latitude']
        self.iss_long = self.req_json['iss_position']['longitude']

    def move(self,):
        self.goto(self.x, self.y)

    def get_position(self):
        return self.x, self.y

    def set_grid_position(self):
        self.y = int(float(format(self.req_json['iss_position']['latitude'])) * 2.5)
        self.x = int(float(format(self.req_json['iss_position']['longitude'])) * 2.5)

    def get_gps(self):
        return self.iss_lat, self.iss_long
