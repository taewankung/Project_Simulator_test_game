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
        self.controller.buy_item('Potion',"start")
        self.controller.move(500,300,"end lane")
        while self.controller.get_connection():
            hero_status = self.controller.status
            item_list = self.controller.get_item_in_hero()
            hero_gold = self.controller.get_gold()
            near_enemy = self.controller.get_near_enemy()
            recive_message = self.controller.get_rev_message()

            if recive_message =='start':
                self.controller.move(500,300,"end lane")
            if recive_message == 'found_enemy':
                if len(near_enemy) !=0:
                    self.controller.attack(near_enemy[0],'start')
                else:
                    self.controller.move(500,300,"end_lane")
            if recive_message == 'battle':
                if len(near_enemy) !=0:
                    self.controller.use_skill(1,near_enemy[0],'battle')
                    self.controller.attack(near_enemy[0],'start')
                    if self.controller.get_hp_percent()<=0.5:
                        self.controller.use_item('Potion','battle')
                else:
                    self.controller.move(500,300,"end_lane")

            if recive_message == 'reborn':
                if 'Potion' not in item_list and hero_gold > 100:
                    self.controller.buy_item('Potion','start')
                self.controller.move(500,300,"end lane")
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
        self.controller.alliance_message('go go go')

    def run(self):
        self.upgrade_skill()
        self.move()
