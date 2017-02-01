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
        self.controller.move(1000,1000,"end lane")
        while self.controller.connection_status:
            hero_status = self.controller.status
            item_list = [i['name'] for i in hero_status['item']]
            if self.controller.rev_message == 'start':
                self.controller.move(1000,1000,"end lane")
            if self.controller.rev_message == 'found_enemy':
                if len(hero_status['near_enemy_list']) !=0:
                    self.controller.attack(hero_status['near_enemy_list'][0],'start')
                else:
                    self.controller.move(1000,1000,"end_lane")
            if self.controller.rev_message == 'battle':
                if len(hero_status['near_enemy_list']) !=0:
                    self.controller.use_skill(1,hero_status["near_enemy_list"][0],'battle')
                    self.controller.attack(hero_status['near_enemy_list'][0],'start')
                    if self.controller.get_hp_percent()<=0.5:
                        self.controller.use_item('Potion','battle')
                else:
                    self.controller.move(1000,1000,"end_lane")
            if self.controller.rev_message == 'reborn':
                if 'Potion' not in hero_status['item'] and hero_status['gold']>100:
                    self.controller.buy_item('Potion','start')
                self.controller.move(1000,1000,"end lane")
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


            #  if self.controller.rev_message == "found_enemy":
                #  if len(hero_status["near_enemy_list"]) !=0:
                    #  self.controller.use_skill(1,hero_status["near_enemy_list"][0],"start")
                    #  self.controller.attack(hero_status["near_enemy_list"][0],"start")
            #  if self.controller.rev_message == "battle":
                #  if hero_status['current_hp']/hero_status['max_hp']*100<=0.30:
                    #  if 'Potion' in hero_status['item_list']:
                        #  self.controller.use_item('Potion')
                    #  else:
                        #  self.controller.buy_item('Potion')
                #  if len(hero_status["near_enemy_list"]) !=0:
                    #  self.controller.attack(hero_status["near_enemy_list"][0],"start")
                    #  time.sleep(0.001)
                    #  self.controller.use_skill(1,hero_status["near_enemy_list"][0],"start")
            #  if self.controller.rev_message == "can_not_use_skill":
                #  if len(hero_status["near_enemy_list"]) !=0:
                    #  self.controller.attack(hero_status["near_enemy_list"][0])
            #  if self.controller.rev_message == 'reborn':
                #  if hero_status['alive']:
                    #  self.controller.move(1000,1000,"come_to_duel")
