# import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from time import sleep
from rich import print
from rich.console import Console
from rich.traceback import install
from src.Client import Client
from src.Odometry import Odometry

console = Console()
install() # install rich traceback

#class SubOdometry(threading.Thread):
#    def __init__(self, normalize_factor:int = 1):
#        self.normalize_factor = normalize_factor


def test():
    plt.ion()
    client = Client()
    odo = Odometry()
    client.loop_start()
    angular_dis = None
    x_glob = np.array([])
    y_glob = np.array([])
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #sc = ax.scatter(x_glob, y_glob)
    #plt.draw()
    while True:
        try:
            ret = client.sub(['AngularDistance'])
            if ret['AngularDistance'] != None:
                console.log(log_locals=True)
                angular_dis = ret['AngularDistance']
                points = odo.transform2cartesian(angular_dis)
                # print(points[250].x, points[250].y)
                xs = np.array([])
                ys = np.array([])
                for point in points:
                    xs = np.append(xs, point.x)
                    ys = np.append(ys, point.y)
                if len(x_glob) == 0:
                    x_glob = xs
                    continue
                if len(y_glob) == 0:
                    y_glob = ys
                    continue
                x_glob = np.stack((x_glob, xs), axis=0)
                y_glob = np.stack((y_glob, ys), axis=0)
                #sc.set_offsets(np.c_[x_glob, y_glob])
                #fig.canvas.draw_idle()
                #plt.pause(.1)
            sleep(1)
        except KeyboardInterrupt:
            console.log(x_glob.shape, x_glob)
            break

if __name__ == '__main__':
    test()
