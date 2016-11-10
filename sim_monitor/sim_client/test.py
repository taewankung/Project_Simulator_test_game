import importlib
import os
import subprocess
import inspect
import sys
from .api_game.apaimanee import HeroController
from .api_game.my_hero import MyHero
import time

class x(MyHero):
    def __init__(self):
        super().__init__()
        self.controller = HeroController()
        self.status = self.controller.status
        time.sleep(5)
        pass

    def move(self):
        #if self.controller.ac.game_logic.game_space[""]
        self.status = self.controller.status
        self.controller.move(500,550,"func1")
        #print("{0},{1}".format(self.status["pos_y"],self.status["pos_y"]))
        while True:
            if self.controller.rev_message == "func1":
                self.controller.move(300,350,"func2")
            if self.controller.rev_message == "func2":
                self.controller.move(300,550,"func3")
            if self.controller.rev_message == "func3":
                self.controller.move(320,450,"func4")
            if self.controller.rev_message == "func4":
                self.controller.move(500,550,"func1")
            self.controller.update_message()
            time.sleep(1)

    def run(self):
        self.move()


#  if __name__== "__main__":
    #  test = __import__("executor","..")
    #  for name, obj in inspect.getmembers(test):
        #  if inspect.isclass(obj):
            #  print(obj)
     #  test.x()
