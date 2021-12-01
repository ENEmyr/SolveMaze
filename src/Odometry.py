import numpy as np
from numpy import pi, cos, sin
from typing import Union, List
from src.Client import Client
from rich.console import Console
from rich.traceback import install

console = Console()
install() # install rich traceback

class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

class Odometry:
    def __init__(self) -> None:
        self.angular_dis = []
    def transform2cartesian(self, distances:Union[str, List[int]]) -> list:
        if type(distances) == str:
            distances = distances.replace('[', '').replace(']', '').split(',')
            distances = (np.array(distances)).astype('int')
        elif type(distances) == list:
            distances = np.array(distances).astype('int')
        else:
            raise ValueError('Wrong argument type.')
        self.angular_dis = distances
        points = []
        for angle in range(len(self.angular_dis)):
            x = (80+(self.angular_dis[angle]/70)*cos(pi*angle/180+.13))*2
            y = (100+(self.angular_dis[angle]/70)*sin(pi*angle/180+.13))*2
            points.append(Point(x, y))
        return points

