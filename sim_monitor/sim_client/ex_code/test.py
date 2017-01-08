import importlib
import os
import subprocess
import inspect
import sys
from sim_monitor.sim_client.api_game.hero_controller import HeroController
from sim_monitor.sim_client.api_game.my_hero import MyHero
import time

class x(MyHero):
    def __init__(self):
        super().__init__()
        self.controller = HeroController()
        time.sleep(5)

    def move(self):
        #if self.controller.ac.game_logic.game_space[""]
        self.controller.move(1000,1000,"start")
        #print("{0},{1}".format(self.status["pos_y"],self.status["pos_y"]))
        while True:
            self.status = self.controller.status
            if self.controller.rev_message == "start":
                self.controller.move(20,20,"go_to_20_20")
            if self.controller.rev_message == "go_to_20_20":
                self.controller.move(500,1000,"go_to_500_1000")
            if self.controller.rev_message == "go_to_500_1000":
                self.controller.move(500,250,"go_to_500_250")
            if self.controller.rev_message == "go_to_500_250":
                self.controller.move(100,250,"go_to_100_250")
            if self.controller.rev_message == "found_enemy":
                #print(self.status["near_enemy_list"])
                if len(self.status["near_enemy_list"]) !=0:
                    self.controller.attack(self.status["near_enemy_list"][0],"attack")
                #self.controller.move(10,250,"start")
                #print(self.status["near_enemy"])
                #self.controller.rev_message = ""
 #           if self.controller.rev_message == 'died':
#                print(self.status['gold'])
            if self.controller.rev_message == 'reborn':
                if self.status['alive']:
                    self.controller.move(1000,1000,"start")


            self.controller.update_message()
            #print(self.controller.rev_message)
            self.controller.update_status()
            time.sleep(0.01)

    def run(self):
        self.move()


#  if __name__== "__main__":
    #  test = __import__("executor","..")
    #  for name, obj in inspect.getmembers(test):
        #  if inspect.isclass(obj):
            #  print(obj)
     #  test.x()
