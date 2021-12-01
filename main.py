# from src.Client import Client
from icecream import ic
from src.ClientAnto import ClientAnto as Client
from src.Odometry import Odometry
from configs import MQTTConfig

def test():
    config = MQTTConfig()
    ic(config.SubTopics)

def main():
    client = Client(subs=['Maze_Distance'])
    def on_run():
        try:
            distances = client.sub("Maze_Distance")
            if distances != None:
                if type(distances) == bytes:
                    distances = distances.decode('utf-8')
                    return distances
            else:
                # print("Idle")
                pass
            sleep(1)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
    client.connect(on_run)
    odo = Odometry(client)
    distances = odo.get_distances()
    points = odo.transform2cartesian(distances)
    print(odo)

if __name__ == '__main__':
    test()
