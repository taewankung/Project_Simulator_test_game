import importlib
import os
import subprocess
import inspect
import sys
from .api_game.apaimanee import HeroController
from .api_game.my_hero import MyHero

class x(MyHero):
    def __init__(self):
        super().__init__()
        self.controller = HeroController()
        self.status = self.controller.status
        pass
    def move(self):
        #if self.controller.ac.game_logic.game_space[""]
        self.status = self.controller.status
        if (self.status["pos_x"]-500 < -0.1 or self.status["pos_x"]-500 > 0.1) or \
           (self.status["pos_y"]-550 < -0.1 or self.status["pos_y"]-550 > 0.1) :
            self.controller.move(500,550)
            print("{0},{1}".format(self.status["pos_y"],self.status["pos_y"]))
        else:
            self.controller.move(300,750)
        pass

    def run(self):
#        print("i will move")
        self.move()

#  if __name__== "__main__":
    #  test = __import__("executor","..")
    #  for name, obj in inspect.getmembers(test):
        #  if inspect.isclass(obj):
            #  print(obj)
     #  test.x()
