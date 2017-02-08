from __future__ import division, print_function, unicode_literals
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
import sys
import os
from pyglet.gl import *
import cocos
import pyglet
from cocos.menu import *
from cocos.text import *
from cocos.layer import *
from cocos.actions import *

from sim_monitor.model.status import status
from .bar import Bar

import subprocess
from multiprocessing import Process
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class SummaryBackground(cocos.layer.ColorLayer):
    def __init__(self, r, b, g, a, team="Team1", width=0, height=0):
        super().__init__(r,b,g,a, width=width, height=height)
        self.status_dict = {}
        self.ac = ApaimaneeMOBAClient()
        self.count_hero_team1 = 0
        self.count_hero_team2 = 0
        self.status_hero_team1 = {}
        self.status_hero_team2 = {}
        self.team = team

        self.hero_team1 = {}
        self.hero_team2 = {}
        self.img = pyglet.resource.image('sim_monitor/res/result_team1-2.png')

        if self.team == 'Team2':
            self.img = pyglet.resource.image('sim_monitor/res/result_team2-2.png')

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(-5, -20)
        glPopMatrix()

    def load_hero(self):
        count = 0
        if self.team == 'Team1':
            for hero in self.ac.game_logic.game_space['hero_team1']:
                name = self.ac.game_logic.game_space['hero_team1'][hero]['name']
                #button= Button(255,100,100,100,hero,"")
                self.status_hero_team1[name] = HeroLayer(name,'team1',hero, self.x, self.y-(50*count))
                self.status_hero_team1[name].position = (0,600-(50*count))
                self.add(self.status_hero_team1[name])

                count = count + 1

        count = 0
        if self.team == 'Team2':
            for hero in self.ac.game_logic.game_space['hero_team2']:
                name = self.ac.game_logic.game_space['hero_team2'][hero]['name']
                self.status_hero_team2[name] = HeroLayer(name, 'team2',hero, self.x, self.y-(50*count))
                self.status_hero_team2[name].position = (0,600-(50*count))
                self.add(self.status_hero_team2[name])
                count = count + 1


class HeroLayer(cocos.layer.ColorLayer):

    def __init__(self, name,team, hero_key,local_x, local_y, width=500, height=200 ,r=0, b=0, g=0, a=0):
        super().__init__(r,b,g,a, width=width, height=height)

        #self.is_event_handler = True
        self.hero_key = hero_key
        self.ac = ApaimaneeMOBAClient()
        self.team = team
        self.local_x = local_x
        self.local_y = local_y
        self.timer = 0
        self.data = self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key]
        self.text_name = cocos.text.Label('Name', font_size = 17, bold= True)
        self.text_tblv = cocos.text.Label('Level', font_size = 17, bold= True)
        self.text_tbgold = cocos.text.Label('Gold', font_size = 17, bold= True)
        self.text_tbkda = cocos.text.Label('K/D/A', font_size = 17, bold= True)
        self.text_tbitem = cocos.text.Label('Item', font_size = 17, bold= True)

        self.text_hero = cocos.text.Label(name, font_size = 15)
        self.text_level = cocos.text.Label('{}'.format(self.data['level']) , font_size = 12, bold= True)
        self.text_kill = cocos.text.Label('{}/ '.format(self.data['kill']), font_size = 12, bold= True)
        self.text_death = cocos.text.Label('{}/0'.format(self.data['death']) , font_size = 12, bold= True)
        self.text_gold = cocos.text.Label('{}'.format(self.data['gold']), font_size = 12, bold=True)
        self.text_item = cocos.text.Label('{}'.format([i['name'] for i in self.data['item']]), font_size = 12, bold= True)

        self.text_name.position = (15,20)
        self.text_tblv.position = (200, 20)
        self.text_tbgold.position = (300, 20)
        self.text_tbkda.position = (400, 20)
        self.text_tbitem.position = (600, 20)
        self.text_hero.position = (20, -40)
        self.text_level.position = (200, -40)
        self.text_kill.position = (400, -40)
        self.text_death.position = (415, -40)
        self.text_item.position = (480, -40)
        self.text_gold.position = (290, -40)

        # self.add(self.text_name,1)
        # self.add(self.text_tblv, 1)
        # self.add(self.text_tbgold, 1)
        # self.add(self.text_tbkda, 1)
        # self.add(self.text_tbitem,1)

        self.add(self.text_hero,1)
        self.add(self.text_level,1)
        self.add(self.text_kill,1)
        self.add(self.text_death,1)
        self.add(self.text_item, 1)
        self.add(self.text_gold, 1)




class Button(cocos.layer.ColorLayer):
    def __init__(self,r, b, g, a,name,width=190, height=50):
        super().__init__(r, b, g, a, width=width, height=height)
        self.is_event_handler = True
        self.local_x = 0
        self.local_y = 0
        self.name = cocos.text.Label(name, font_size = 20)
        self.name.position = (40,13)
        self.add(self.name)

        self.img = pyglet.resource.image('sim_monitor/res/buttonkivy.png')

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()

    def set_local(self, local_x, local_y):
        self.local_x = local_x
        self.local_y = local_y

    def on_mouse_press(self, x, y, buttons, modifiers):
        print(str(self.local_x) +' '+ str(self.local_y))
        print(str(x) +' '+ str(y))
        if (x >=self.local_x and x <=(self.local_x+150)  and y >= (self.local_y) and y <= (self.local_y+50)):
            self.on_quit()

    def on_quit(self):
        ac = ApaimaneeMOBAClient()
        data = dict(client_id=ac._client_id,
                    token_id=ac.game_client.user.loggedin_info['token'],
                    page='lobby',
                    host=ac.game_client._host)
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)
        pyglet.app.exit()


class DisplaySummaryLayer(cocos.layer.ColorLayer):
    def __init__(self,r, b, g, a,width=800, height=900):
        super().__init__(r, b, g, a, width=width, height=height)
        self.ac = ApaimaneeMOBAClient()

        self.game_space = self.ac.game_logic.game_space

        self.img = pyglet.resource.image('sim_monitor/res/show_status.png')
        self.is_event_handler = True
        self.timer = 0


    #  def draw(self):
        #  glPushMatrix()
        #  self.transform()
        #  self.img.blit(0, 0)
        #  glPopMatrix()
