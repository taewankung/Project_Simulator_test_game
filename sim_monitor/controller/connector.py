import time
import datetime
from threading import Thread

from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.sim_client.connection import initial_game
from sim_monitor.model.status import status
from sim_monitor.sim_client.executor import Executor

class Connector(Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.ac = None
        self.ex = None
        self.ex_file = ""

    def run(self):
        print("connecting")
        self.connect()
        self.ac = ApaimaneeMOBAClient()
        self.ac.game_client.game.update()
        self.ex.load_file(self.ex_file)
#        print(status.connect)
#        while(status.connect):
        self.ex.run()
            #  for hero in self.ac.game_logic.game_space["hero_team1"]:
                #  print(self.ac.game_logic.game_space["hero_team1"][hero]["pos_x"])


    def connect(self):
        global send_initial
        send_initial = False
        start_time = None
        while not status.connect:
            if start_time is not None:
                ac = ApaimaneeMOBAClient()
                if ac.game_logic.status == 'play':
                    print("//////////////////PLAY/////////////////")
                    status.connect = True
                    self.ex = Executor()
                diff_time = datetime.datetime.now() - start_time
                time.sleep(1)
                print('wait for play singnal', diff_time.seconds)
                if diff_time.seconds % 20 == 0:
                    if not send_initial:
                        ac.game_client.game.initial()
                        send_initial = True
                else:
                    send_initial = False
                if diff_time > datetime.timedelta(minutes=2):
                    print('time out')
                    ac.disconnect()
            else:
                try:
                    self.ex_file = initial_game()
                except Exception as e:
                    print('Initial Fail:', e)
                start_time = datetime.datetime.now()

    def disconnect(self):
        try:
            self.ac.disconnect()
            status.connect = False
        except Exception as e:
            print("Exeption conector: "+e)
            print("apaimanee client not load or haven't connection")

