import subprocess, optparse
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from time import sleep
from rich import pretty
from rich.console import Console
from rich.traceback import install
from rich.progress import track
from src.Client import Client
from src.Odometry import Odometry
from src.Mapper import Mapper

console = Console()
pretty.install()
install() # install rich traceback

def run(
        solve_mode:bool = True,
        maze_size:int = 6,
        block_length:int = 400,
        tick_rate:float = .1,
        show_maze:bool = True,
        dynamic_update_maze:bool = False,
        debug_mode:bool = False
        ):
    # TODO: dynamictically update explored map, fix solver
    client = Client()
    mapper = Mapper(maze_size=maze_size, padd=True)
    odo = Odometry()
    client.loop_start()
    _entrance_exit = None
    console.print('\nEstasblishing connection to MQTT Broker\n', style='bold cyan')
    for step in track(range(5)):
        sleep(.1)
    else:
        client.pub({'AngularDistance':'','StopExplore':'','EntranceExit':'','Command':''})
    try:
        # console.print('Step 1: Mapping\n', style='bold cyan')
        with console.status("[bold cyan]Step 1: Mapping") as status:
            while True:
                ret = client.sub(['AngularDistance', 'StopExplore'])
                if ret['StopExplore'] != None:
                    console.print(' > Stop Mapping', style='red')
                    client.pub({'StopExplore': ''})
                    sleep(.2)
                    if debug_mode:
                        console.log('Stop Exploring', log_locals=True)
                    break
                if ret['AngularDistance'] != None:
                    console.print(' > Mapping Local...', style='yellow')
                    client.pub({'AngularDistance': ''})
                    sleep(.2)
                    if debug_mode:
                        console.log('Put Map', log_locals=True)
                    forward_distance, rotate_angle = odo.minimum_forward_distance(ret['AngularDistance'])
                    mapper.map(forward_distance, rotate_angle, block_length)
                sleep(tick_rate)
    except KeyboardInterrupt:
        client.pub({'AngularDistance':'','StopExplore':'','EntranceExit':'','Command':''}, verbose=debug_mode)
    with console.status("[bold cyan]Step 2: Constructing a maze") as status:
    # console.print('Step 2: Contructing a maze\n', style='bold cyan')
        maze = mapper.construct()
        max_col = maze.shape[0]
        if show_maze:
            # plt.axis('off')
            plt.imshow(maze, cmap='Greys', interpolation='none')
            plt.savefig('Maze.png')
            plt.waitforbuttonpress()
            if debug_mode:
                console.log('Map Contructed', log_locals=True)
    if solve_mode:
        try:
            with console.status("[bold cyan]Step 3: Waiting for define an entrnace and exit of the maze") as status:
            # console.print('Step 3: Waiting for define entrance and exit of the maze\n', style='bold cyan')
                while True:
                    ret = client.sub(['EntranceExit'])
                    if ret['EntranceExit'] != None:
                        if debug_mode:
                            console.log('Got Entrance and Exit', log_locals=True)
                        console.print(' > Entrance & Exit was Defined', style='green')
                        _entrance_exit = ret['EntranceExit'].split('|') # in form : aa, bb | cc, dd
                        client.pub({'EntranceExit': ''})
                        sleep(.2)
                        break
                    else:
                        if debug_mode:
                            console.log(ret, log_locals=True)
                    sleep(tick_rate)
        except KeyboardInterrupt:
            client.pub({'AngularDistance':'','StopExplore':'','EntranceExit':'','Command':''}, verbose=debug_mode)
            with open('constructed_maze.npy', 'wb') as f:
                np.save(f, maze, allow_pickle=True)
        with console.status("[bold cyan]Step 4: Solve the maze") as status:
        # console.print('Step 4: Solve the maze\n', style='bold cyan')
            _entrance = list(map(lambda x: int(x), _entrance_exit[0].split(',')))
            _exit = list(map(lambda x: int(x), _entrance_exit[1].split(',')))
            maze = np.where(maze>0, -1, maze)
            maze = np.where(maze==0, 1, maze)
            maze = np.where(maze==-1, 0, maze).flatten().astype('int')
            maze_str = ''
            i = 0
            row = 0
            col = 0
            for x in maze:
                if row == _entrance[0] and col == _entrance[1]:
                    maze_str += 's'
                elif row == _exit[0] and col == _exit[1]:
                    maze_str += 'f'
                else:
                    maze_str += f'{x}'
                i += 1
                col += 1
                if i == max_col:
                    maze_str += '\n'
                    i = 0
                    row += 1
                    col = 0
            _entrance = ','.join([str(x) for x in _entrance])
            if debug_mode:
                console.print('Maze Map :\n', maze_str)
            p = subprocess.Popen(['node', './solver.js', f'--maze={maze_str}', f'--entrance={_entrance}'], stdout=subprocess.PIPE)
            output = p.stdout.read()
            commands = output.decode('utf-8').replace('\n', '').split(',')
            commands = commands[::-1] # transform queue -> stack
            latest_command = ''
            if debug_mode:
                console.log('Solved', log_locals=True)
        try:
            with console.status("[bold cyan]Step 5: Commanding Robot") as status:
            # console.print('Step 5: Commanding Robot', style='bold cyan')
                while True:
                    ret = client.sub(['Command'])
                    if ret['Command'] != None and ret['Command'] != latest_command:
                        latest_command = commands.pop()
                        console.print(f' > {latest_command}', style='yellow')
                        client.pub({'Command': latest_command}, verbose=debug_mode)
                        sleep(.2)
                    if len(commands) == 0:
                        console.print('Finished!!', style='bold green')
                        break
                    sleep(tick_rate)
        except KeyboardInterrupt:
            client.pub({'AngularDistance':'','StopExplore':'','EntranceExit':'','Command':''}, verbose=debug_mode)
        client.pub({'AngularDistance':'','StopExplore':'','EntranceExit':'','Command':''}, verbose=debug_mode)

options = [
        optparse.make_option('-s', '--solve', action='store_true', dest='solve_mode', help='solve the contracted maze or not', default=False),
        optparse.make_option('-m', '--maze-size', type='int', dest='maze_size', help='size of the maze in blocks', default=6),
        optparse.make_option('-b', '--block-length', type='int', dest='block_length', help='length of a single block', default=400),
        optparse.make_option('-t', '--tick-rate', type='float', dest='tick_rate', help='wait for \'tick rate\' second to send another request to MQTT Broker', default=.1),
        optparse.make_option('--show-maze', action='store_true', dest='show_maze', help='show constructed maze or not', default=False),
        optparse.make_option('--dynamic-update-maze', action='store_true', dest='dynamic', help='show constructed maze dynamictically', default=False),
        optparse.make_option('--debug', action='store_true', dest='debug', help='debug mode', default=False),
    ]
parser = optparse.OptionParser(option_list=options)

if __name__ == '__main__':
    (options, args) = parser.parse_args()
    run(
        options.solve_mode, 
        options.maze_size, 
        options.block_length,
        options.tick_rate,
        options.show_maze, 
        options.dynamic, 
        options.debug)
