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

    def move(self):
        #if self.controller.ac.game_logic.game_space[""]
        self.controller.move(500,350,"come_to_duel")
        while True:
            #status = self.controller.status
            if self.controller.rev_message == "found_enemy":
      #          print([u for u in self.status["near_enemy_list"]])
                if len(status["near_enemy_list"]) !=0:
                    self.controller.attack(status["near_enemy_list"][0])
            if self.controller.rev_message == "battle":
                if len(status["near_enemy_list"]) !=0:
                    self.controller.attack(status["near_enemy_list"][0])
                    time.sleep(0.001)
                    self.controller.use_skill(1,status["near_enemy_list"][0],"start")
            if self.controller.rev_message == "can_not_use_skill":
                if len(status["near_enemy_list"]) !=0:
                    self.controller.attack(status["near_enemy_list"][0])
            if self.controller.rev_message == 'reborn':
                if status['alive']:
                    self.controller.move(500,450,"come_to_duel")

            self.controller.update_message()
            self.controller.update_status()
            time.sleep(0.01)

    def upgrade_skill(self):
#        time.sleep(1)
#        self.controller.select_hero('Sinsamut')
        time.sleep(1)
        self.controller.upgrade_skill(1)
        time.sleep(3)

    def run(self):
        self.upgrade_skill()
        self.move()


#  if __name__== "__main__":
    #  test = __import__("executor","..")
    #  for name, obj in inspect.getmembers(test):
        #  if inspect.isclass(obj):
            #  print(obj)
     #  test.x()
