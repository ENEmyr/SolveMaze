# import threading
import numpy as np
from typing import Tuple
# from time import sleep
# from rich import print
from rich.console import Console
from rich.traceback import install

console = Console()
install() # install rich traceback

class Mapper:
    def __init__(self) -> None:
        self.__ref_point = 0
        self.__old_ref_point = 0
        # self.__turn_flag = 0
        self.__cache_flag = 0
        self.__old_cache_flag = 0
        self.__cache_dir = 0
        self.x_glob = np.array([])
        self.y_glob = np.array([])

    def map(self, xs:np.ndarray, ys:np.ndarray, turn_direction:int) -> None:
        try:
            self.__cache_flag += np.abs(turn_direction/90)
            self.__cache_dir = turn_direction/90
            if len(self.x_glob) == 0 and len(self.y_glob) == 0:
                self.x_glob = xs.copy()
                self.y_glob = ys.copy()
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
                diff_x = np.abs(xs[270] - self.x_glob[270])
                diff_y = np.abs(ys[270] - self.y_glob[270])
            else:
                if turn_direction != 0:
                    diff_x = np.abs(xs[270] - self.x_glob[self.__old_ref_point][270])
                    diff_y = np.abs(ys[270] - self.y_glob[self.__old_ref_point][270])
                else:
                    diff_x = np.abs(xs[270] - self.x_glob[self.__ref_point][270])
                    diff_y = np.abs(ys[270] - self.y_glob[self.__ref_point][270])
            if self.__cache_dir > 0:
                if turn_direction != 0:
                    xs -= diff_x
                    ys -= diff_y
                xs += diff_x
                ys -= diff_y
                # ys *= 0
            elif self.__cache_dir < 0:
                if turn_direction != 0:
                    xs += diff_x
                    ys -= diff_y
                xs -= diff_x
                ys -= diff_y
                # ys *= 0
            else:
                # self.__cache_dir == 0
                xs += diff_x
                # xs *= 0
                ys -= diff_y
            if self.__cache_flag % 2 == 0:
                self.x_glob = np.vstack((self.x_glob, xs))
                self.y_glob = np.vstack((self.y_glob, ys))
            else:
                self.x_glob = np.vstack((self.x_glob, ys))
                self.y_glob = np.vstack((self.y_glob, xs))
            console.log('Putted')
        except Exception as e:
            console.log(log_locals=True)


    def construct(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.x_glob, self.y_glob
