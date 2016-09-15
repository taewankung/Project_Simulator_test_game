import inspect
import importlib
from .api_game.my_hero import MyHero


class Executor:
    def __init__(self):
        self.ex_lib = None
        self.hero = MyHero()

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
        try:
            self.hero.run()
        except Exception as e :
            print(e)
        pass


#  if __name__ == "__main__":
      #  ex = Executor("api_game.apaimanee","api_game")
      #  ex.run()
