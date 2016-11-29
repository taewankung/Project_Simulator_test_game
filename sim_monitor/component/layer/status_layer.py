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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



class StatusBackground(cocos.layer.ColorLayer):
    def __init__(self, r, b, g, a, team="", width=0, height=0):
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
        

    def load_hero(self):
        count = 0
        if self.team == 'Team1':
            for hero in self.ac.game_logic.game_space['hero_team1']:
                name = self.ac.game_logic.game_space['hero_team1'][hero]['name']
                button= Button(255,100,100,100,hero,"Status")
                self.status_hero_team1[name] = StatusLayer(name, button, 'team1',hero, self.x+(200*count), self.y)
                self.status_hero_team1[name].position = (200*count,0)
                self.add(self.status_hero_team1[name])

                #self.text_hero_team1[name] = cocos.text.Label(name, font_size = 20, x=50+count*200, y=1024)
                count = count + 1
                print(name)

        count = 0
        if self.team == 'Team2':
            for hero in self.ac.game_logic.game_space['hero_team2']:
                name = self.ac.game_logic.game_space['hero_team2'][hero]['name']
                #self.text_hero_team2[name] = cocos.text.Label(name, font_size = 20, x=50+count*200, y=150)
                button = Button(255,100,100,100,hero,"Status")
                self.status_hero_team2[name] = StatusLayer(name, button, 'team2',hero, self.x+(200*count), self.y)
                self.status_hero_team2[name].position = (200*count,0)
                self.add(self.status_hero_team2[name])
                count = count + 1


class StatusLayer(cocos.layer.ColorLayer):

    def __init__(self, name, button, team, hero_key,local_x, local_y, width=200, height=200 ,r=0, b=0, g=0, a=0):
        super().__init__(r,b,g,a, width=width, height=height)
        self.text_hero = cocos.text.Label(name, font_size = 20)
        self.text_hp = cocos.text.Label('HP: ', font_size = 15)
        self.text_mana = cocos.text.Label('MANA: ', font_size = 15)
        self.is_event_handler = True
        self.hero_key = hero_key
        self.ac = ApaimaneeMOBAClient()
        self.team = team
        self.button = button
        self.local_x = local_x
        self.local_y = local_y
        self.timer = 0

        self.text_hero.position = (0, 150)
        self.text_hp.position = (0, 120)
        self.text_mana.position = (0, 100)
        self.button.set_local(self.local_x+self.x, self.local_y+self.y)
        self.button.position=(5,0)  
        self.add(self.text_hero,1)
        self.add(self.text_hp,1)
        self.add(self.text_mana,1)
        self.add(self.button,0)

        self.schedule(self.step)
        print(self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key])


    def update_status(self):
        

        hp = self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key]['current_hp']
        mana = self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key]['current_mana']
        self.text_hp.element.text = 'HP: ' + str(hp)
        self.text_mana.element.text = 'MANA: ' + str(mana)

    def step(self, dt):
        self.timer += dt
        if self.timer > 0.01:
            self.timer = 0
            self.update_status()

     
class Button(cocos.layer.ColorLayer):
    def __init__(self,r, b, g, a,hero_key,name,width=190, height=50):
        super().__init__(r, b, g, a, width=width, height=height)
        self.hero_key = hero_key
        self.is_event_handler = True
        self.local_x = 0
        self.local_y = 0
        self.name = cocos.text.Label(name, font_size = 20)
        self.name.position = (55,5)
        self.add(self.name)

    def set_local(self, local_x, local_y):
        self.local_x = local_x
        self.local_y = local_y

    def on_mouse_press(self, x, y, buttons, modifiers):
        print(str(self.local_x) +' '+ str(self.local_y))
        print(str(x) +' '+ str(y))
        if (x >=self.local_x and x <=(self.local_x+150)  and y >= (self.local_y) and y <= (self.local_y+50)):
#            print(self.hero_key) 
            self.on_show_status()
            
    def on_quit(self):
        pyglet.app.exit()

    def on_show_status(self):
        status.hero_key = self.hero_key
        #text = '%d,%d' % (x, y)
        #self.name.element.text = text
        pass

    

class DisplayStatusLayer(cocos.layer.ColorLayer):
    def __init__(self,r, b, g, a,width=800, height=900):
        super().__init__(r, b, g, a, width=width, height=height)
        self.ac = ApaimaneeMOBAClient()
        self.game_space = self.ac.game_logic.game_space
        self.text_name = cocos.text.Label('Name: ', font_size = 20)
        self.text_hp = cocos.text.Label('HP: ', font_size = 15)
        self.text_mana = cocos.text.Label('MANA: ', font_size = 15)
        self.is_event_handler = True
        self.timer = 0
        self.text_name.position = (0, 760)
        self.text_hp.position = (0, 720)
        self.text_mana.position = (0, 700)

#       add text        
        self.add(self.text_name,1)
        self.add(self.text_hp,1)
        self.add(self.text_mana,1)

        self.schedule(self.step)

    def update_status(self):
        if status.hero_key != None:
            if status.hero_key in self.game_space['hero_team1']:
                name = self.game_space['hero_team1'][status.hero_key]['name']
                hp = self.game_space['hero_team1'][status.hero_key]['current_hp']
                mana = self.game_space['hero_team1'][status.hero_key]['current_mana']
                self.text_name.element.text = 'Name: ' + str(name)
                self.text_hp.element.text = 'HP: ' + str(hp)
                self.text_mana.element.text = 'MANA: ' + str(mana)


    def step(self, dt):
        self.timer += dt
        if self.timer > 0.01:
            self.timer = 0
            self.update_status()