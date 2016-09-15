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
        pass
    def move(self):
        self.controller.move(500,550)
        pass

    def run(self):
        print("i will move")
        self.move()

#  if __name__== "__main__":
    #  test = __import__("executor","..")
    #  for name, obj in inspect.getmembers(test):
        #  if inspect.isclass(obj):
            #  print(obj)
     #  test.x()
