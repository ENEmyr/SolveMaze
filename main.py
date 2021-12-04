from time import sleep
import matplotlib.pyplot as plt
from time import sleep
from rich.console import Console
from rich.traceback import install
from src.Client import Client
from src.Odometry import Odometry
from src.Mapper import Mapper

console = Console()
install() # install rich traceback

def main():
    block_length = 400
    client = Client()
    mapper = Mapper(maze_size=12, padd=True)
    odo = Odometry()
    client.loop_start()
    try:
        while True:
            ret = client.sub(['AngularDistance', 'StopExplore'])
            if ret['StopExplore'] != None:
                break
            if ret['AngularDistance'] != None:
                forward_distance, rotate_angle = odo.maximum_forward_distance(ret['AngularDistance'])
                mapper.map(forward_distance, rotate_angle, block_length)
            sleep(.5)
    except KeyboardInterrupt:
        pass
    maze = mapper.construct()
    plt.axis('off')
    plt.imshow(maze, cmap='Greys', interpolation='none')
    plt.waitforbuttonpress()

if __name__ == '__main__':
    main()
