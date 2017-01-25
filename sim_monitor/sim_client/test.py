import importlib
import os
import subprocess
import inspect
import sys
from sim_monitor.sim_client.api_game.hero_controller import HeroController
#from sim_monitor.sim_client.api_game.hero_controller import connection_status
from sim_monitor.sim_client.api_game.my_hero import MyHero
from sim_monitor.model.status import status
import time

class x(MyHero):
    def __init__(self):
        super().__init__()
        self.controller = HeroController()

    def move(self):
        #if self.controller.ac.game_logic.game_space[""]
        self.controller.move(500,350,"come_to_duel")
        while self.controller.connection_status:
            hero_status = self.controller.status
            if self.controller.rev_message == "found_enemy":
      #          print([u for u in self.status["near_enemy_list"]])
                if len(hero_status["near_enemy_list"]) !=0:
                    self.controller.use_skill(1,status["near_enemy_list"][0],"start")
                    self.controller.attack(status["near_enemy_list"][0])
            if self.controller.rev_message == "battle":
                if hero_status['current_hp']/hero_status['max_hp']*100<=0.30:
                    if 'Potion' in hero_status['item_list']:
                        self.controller.use_item('Potion')
                    else:
                        self.controller.buy_item('Potion')
                if len(hero_status["near_enemy_list"]) !=0:
                    self.controller.attack(status["near_enemy_list"][0])
                    time.sleep(0.001)
                    self.controller.use_skill(1,status["near_enemy_list"][0],"start")
            if self.controller.rev_message == "can_not_use_skill":
                if len(hero_status["near_enemy_list"]) !=0:
                    self.controller.attack(status["near_enemy_list"][0])
            if self.controller.rev_message == 'reborn':
                if hero_status['alive']:
                    self.controller.move(500,350,"come_to_duel")
            self.controller.update_message()
            self.controller.update_status()
            time.sleep(0.01)

    def upgrade_skill(self):
#        time.sleep(1)
        time.sleep(2)
        self.controller.upgrade_skill(1)
        time.sleep(1)
        self.controller.buy_item('Boot')
        time.sleep(2)
        self.controller.aliance_message('go go go')

    def run(self):
        self.upgrade_skill()
        self.move()


#  if __name__== "__main__":
    #  test = __import__("executor","..")
    #  for name, obj in inspect.getmembers(test):
        #  if inspect.isclass(obj):
            #  print(obj)
     #  test.x()
