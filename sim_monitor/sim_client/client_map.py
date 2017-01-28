from nagaclient import client as aclient
from .logic import GameLogic
import threading
from .executor import Executor
import time

class Singleton(type):
    def __init__(cls,name,bases,dic):
        super(Singleton,cls).__init__(name, bases, dic)
        cls.instance=None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=super(Singleton,cls).__call__(*args, **kw)
        return cls.instance

class GameLogicMonitor(threading.Thread):
    def __init__(self, game_client, game_logic):
        super().__init__()
        self.game_client = game_client
        self.game_logic = game_logic

        self.running = True

    def run(self):
#        test =True
        while(self.running):
#            print("checking")
            if self.game_client.gm.game_logic is None:
                self.game_client.gm.register(self.game_logic)
                print('register new game logic by GameLogicMonitor')
                #  if test:
                    #  test =False
                    #  print('testing create')
                    #  self.game_client.room.create_room('my_room')

            time.sleep(0.001)

class ApaimaneeMOBAClient(metaclass = Singleton):
    def __init__(self, client_id,
            host='localhost', port=1883,
            room_id=None):
        self._client_id = client_id
        self._host = host
        self._port = port
        self._room_id = room_id
        self.game_client = aclient.NagaClient(self._client_id,
                self._host, self._port)
        self.game_logic = GameLogic(self.game_client)
        self.ex = Executor()

    def connect(self):
        self.game_client.initial(True)
#        self.game_client.room.create_room('check')
        self.game_client.gm.start_game(self._room_id)
        self.game_logic.game_client = self.game_client
        self.game_client.gm.register(self.game_logic)
#        print(self._client_id)
#        self.glm = GameLogicMonitor(self.game_client, self.game_client)
#        self.glm.start()

    def disconnect(self):
        self.game_client.disconnect_game()
#        if self.glm:
#            self.glm.running = False
#            self.glm.join()
#            self.glm = None


