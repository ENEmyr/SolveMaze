# import threading
import numpy as np
import math
from typing import Tuple, overload
# from time import sleep
# from rich import print
from rich.console import Console
from rich.traceback import install

console = Console()
install() # install rich traceback

class Mapper:
    def __init__(self, maze_size:int, padd:bool=True) -> None:
        self.__ref_point = 0
        self.__old_ref_point = 0
        self.__cache_flag = 0
        self.__old_cache_flag = 0
        self.__cache_dir = 0
        self.x_glob = np.array([])
        self.y_glob = np.array([])
        self.__maze_size = maze_size*2
        self.__maze = np.zeros((self.__maze_size, self.__maze_size))
        self.__connected_points = []
        self.__padd = padd
        self.__distance_rescaling_factor = 1

    @overload
    def map(self, forward_distance:int, rotate_angle:int, distance_rescaling_factor:int=1) -> None:
        pass

    @overload
    def map(self, xs:np.ndarray, ys:np.ndarray, rotate_angle:int=0) -> None:
        pass

    def map(self, a, b, c):
        if isinstance(a, int) and isinstance(b, int) and isinstance(c, int):
            self.__distance_rescaling_factor = c
            if a < c-(c*.1): # 10% inaccurate
                a = 0
            # self.__connected_points.append((math.ceil(a/c), b)) # Forward direction algorithm
            self.__connected_points.append((1 if a != 0 else a, b)) # One block direction algorithm
            return None
        elif isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and isinstance(c, int):
            try:
                self.__cache_flag += np.abs(c/90)
                self.__cache_dir = c/90
                if len(self.x_glob) == 0 and len(self.y_glob) == 0:
                    self.x_glob = a.copy()
                    self.y_glob = b.copy()
                    console.log('Putted')
                    return None
                if self.__cache_flag > self.__old_cache_flag:
                    self.__old_cache_flag = self.__cache_flag
                    self.__old_ref_point = self.__ref_point
                    if self.x_glob.ndim == 1:
                        self.__ref_point = len(self.x_glob)/360-1
                    else:
                        self.__ref_point = len(self.x_glob)-1
                if self.x_glob.ndim == 1:
                    diff_x = np.abs(a[270] - self.x_glob[270])
                    diff_y = np.abs(b[270] - self.y_glob[270])
                else:
                    if c != 0:
                        diff_x = np.abs(a[270] - self.x_glob[self.__old_ref_point][270])
                        diff_y = np.abs(b[270] - self.y_glob[self.__old_ref_point][270])
                    else:
                        diff_x = np.abs(a[270] - self.x_glob[self.__ref_point][270])
                        diff_y = np.abs(b[270] - self.y_glob[self.__ref_point][270])
                if self.__cache_dir > 0:
                    if c != 0:
                        a -= diff_x
                        b -= diff_y
                    a += diff_x
                    b -= diff_y
                elif self.__cache_dir < 0:
                    if c != 0:
                        a += diff_x
                        b -= diff_y
                    a -= diff_x
                    b -= diff_y
                else:
                    a += diff_x
                    b -= diff_y
                if self.__cache_flag % 2 == 0:
                    self.x_glob = np.vstack((self.x_glob, a))
                    self.y_glob = np.vstack((self.y_glob, b))
                else:
                    self.x_glob = np.vstack((self.x_glob, b))
                    self.y_glob = np.vstack((self.y_glob, a))
                console.log('Putted')
            except Exception as err:
                console.print(err)
                console.log(log_locals=True)


    def construct(self) -> np.ndarray:
        # Construct maze from datapoint with One block direction algorithm
        if len(self.__connected_points) == 0:
            # return self.x_glob, self.y_glob
            return self.__maze
        row = self.__maze_size//2
        col = self.__maze_size//2
        sum_angle = 0
        for point in self.__connected_points:
            if sum_angle >= 360 or sum_angle <= -360:
                sum_angle = 0
            sum_angle += point[1]
            if point[0] == 0:
                self.__maze[row][col] += 1
                continue
            if np.all(self.__maze == 0):
                self.__maze[row][col] += 1
            for _ in range(1, point[0]+1):
                if sum_angle == 0 or sum_angle == 360 or sum_angle == -360:
                    row -= 1
                    # self.__maze[wall_x][wall_y] = 0
                elif sum_angle == 90 or sum_angle == -270:
                    col += 1
                elif sum_angle == -90 or sum_angle == 270:
                    col -= 1
                elif sum_angle == 180 or sum_angle == -180:
                    row += 1
                else:
                    raise ValueError("Invalid rotate angle : ", sum_angle)
                self.__maze[row][col] += 1
                # console.log(point, self.__maze, log_locals=True)
        # Trimming
        self.__maze = np.delete(self.__maze, np.where(~self.__maze.any(axis=0))[0], axis=1)
        self.__maze = np.delete(self.__maze, np.where(~self.__maze.any(axis=1))[0], axis=0)
        # Padding
        if self.__padd:
            self.__maze = np.pad(self.__maze, pad_width=1, mode='constant', constant_values=0)
        return self.__maze

    # def construct(self) -> np.ndarray:
    #     if len(self.__connected_points) == 0:
    #         # return self.x_glob, self.y_glob
    #         return self.__maze
    #     curr_x = self.__maze_size//2
    #     curr_y = self.__maze_size//2
    #     old_x = curr_x
    #     old_y = curr_y
    #     sum_angle = 0
    #     for point in self.__connected_points:
    #         if sum_angle == 360:
    #             sum_angle = 0
    #         sum_angle += point[1]
    #         if point[0] == 0:
    #             continue
    #         if np.all(self.__maze == 0):
    #             self.__maze[curr_x][curr_y] = 1
    #         for _ in range(1, point[0]+1):
    #             if abs(sum_angle) != 90 and self.__maze[old_x][old_y] > 0:
    #                 backward_blocks = math.ceil(point[0]/self.__distance_rescaling_factor)
    #                 for _ in range(backward_blocks):
    #                     if sum_angle == 0 or sum_angle == 360 or sum_angle == -360:
    #                         curr_x += 1
    #                         old_x = curr_x+1
    #                     elif sum_angle == 180 or sum_angle == -180:
    #                         curr_x -= 1
    #                         old_x = curr_x-1
    #             else:
    #                 old_x = curr_x
    #                 old_y = curr_y
    #                 if sum_angle == 0 or sum_angle == 360 or sum_angle == -360:
    #                     curr_x -= 1
    #                 elif sum_angle == 90:
    #                     curr_y += 1
    #                 elif sum_angle == -90:
    #                     curr_y -= 1
    #                 elif sum_angle == 180 or sum_angle == -180:
    #                     curr_x += 1
    #                 else:
    #                     raise ValueError("Invalid rotate angle")
    #                 self.__maze[curr_x][curr_y] = 1
    #             console.log(self.__maze, log_locals=True)
    #     # Trimming
    #     self.__maze = np.delete(self.__maze, np.where(~self.__maze.any(axis=0))[0], axis=1)
    #     self.__maze = np.delete(self.__maze, np.where(~self.__maze.any(axis=1))[0], axis=0)
    #     # Padding
    #     if self.__padd:
    #         self.__maze = np.pad(self.__maze, pad_width=1, mode='constant', constant_values=0)
    #     return self.__maze
