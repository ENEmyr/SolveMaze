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
    def __init__(self, angular_distances:Union[list, np.ndarray]=None) -> None:
        self.angular_dis = angular_distances

    def __str2list(self, lst_str:str) -> np.ndarray:
        lst = lst_str.replace('[', '').replace(']', '').split(',')
        nd_lst = (np.array(lst)).astype('int')
        return nd_lst

    def transform2cartesian(self, angular_distances:Union[str, List[int]]=None) -> list:
        angular_distances = self.angular_dis if angular_distances == None else angular_distances
        if angular_distances == None:
            raise ValueError('Argument not found.')
        if type(angular_distances) == str:
            angular_distances = self.__str2list(angular_distances)
        elif type(angular_distances) == list:
            angular_distances = np.array(angular_distances).astype('int')
        else:
            raise ValueError('Wrong argument type.')
        points = []
        for angle in range(len(angular_distances[1:])): # index 0 is currently rotate direction
            x = (80+(angular_distances[angle]/70)*cos(pi*angle/180+.13))*2
            y = (100+(angular_distances[angle]/70)*sin(pi*angle/180+.13))*2
            points.append(Point(x, y))
        return points

    def minimum_forward_distance(self, forward_distance:Union[str, List[int]]=None) -> tuple:
        angular_distances = self.angular_dis if forward_distance == None else forward_distance
        if forward_distance == None:
            raise ValueError('Argument not found.')
        if type(forward_distance) == str:
            forward_distance = self.__str2list(forward_distance)
        elif type(forward_distance) == list:
            forward_distance = np.array(forward_distance).astype('int')
        else:
            raise ValueError('Wrong argument type.')
        return (int(forward_distance[1]), int(forward_distance[0]))

    def maximum_forward_distance(self, angular_distances:Union[str, List[int]]=None) -> tuple:
        angular_distances = self.angular_dis if angular_distances == None else angular_distances
        if angular_distances == None:
            raise ValueError('Argument not found.')
        if type(angular_distances) == str:
            angular_distances = self.__str2list(angular_distances)
        elif type(angular_distances) == list:
            angular_distances = np.array(angular_distances).astype('int')
        else:
            raise ValueError('Wrong argument type.')
        return (int(angular_distances[271]), int(angular_distances[0]))

