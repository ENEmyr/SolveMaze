from numpy import pi, cos, sin
# from src.Client import Client
from src.ClientAnto import ClientAnto as Client

class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

class Odometry:
    def __init__(self, client:Client=Client()):
        self.client = client
        self.angular_dis = []
    def get_distances(self):
        self.angular_dis = self.client.sub(['Maze_Distance'])
        print(self.angular_dis)
        return self.angular_dis
    def transform2cartesian(self, distances:list=[]):
        distances = self.angular_dis if len(distances) == 0 else distances
        points = []
        for angle in range(distances):
            x = (80+(distances[angle]/70)*cos(pi*angle/180+.13))*2
            y = (100+(distances[angle]/70)*sin(pi*angle/180+.13))*2
            points.append(Point(x, y))
        return points

