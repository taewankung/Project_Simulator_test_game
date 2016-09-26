import inspect
import importlib
from .api_game.my_hero import MyHero
import datetime
import time
from sim_monitor.model.status import status
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient

class Executor:
    def __init__(self):
        self.ex_lib = None
        self.hero = MyHero()
        self.ready_time = datetime.datetime.now()
        self.ac = ApaimaneeMOBAClient()

    def load_file(self,module=""):
        try:
            self.ex_lib = importlib.import_module(module)
            print("load_module complete")
            for name,obj in inspect.getmembers(self.ex_lib):
                if inspect.isclass(obj) and issubclass(obj,MyHero) and obj is not MyHero:
                    print(obj)
                    self.hero = obj()

        except ValueError:
            print("cannot import module: "+module)
            return self.ex_lib
        return self.ex_lib

    def run(self):
        if status.connect and self.ac.game_logic.status == "play":
            diff_time = datetime.datetime.now() - self.ready_time
            if diff_time.seconds % 1 == 0 and diff_time.seconds >0:
                try:
                    self.hero.run()
                except Exception as e :
                    print(e)
        time.sleep(1)
        pass

#  if __name__ == "__main__":
      #  ex = Executor("api_game.apaimanee","api_game")
      #  ex.run()
