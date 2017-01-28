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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



class StatusBackground(cocos.layer.ColorLayer):
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
        self.img = pyglet.resource.image('sim_monitor/res/team1-1.png')

        if self.team == 'Team2':
            self.img = pyglet.resource.image('sim_monitor/res/team2-1.png')

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
                button= Button(255,100,100,100,hero,"")
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
                button = Button(255,100,100,100,hero,"")
                self.status_hero_team2[name] = StatusLayer(name, button, 'team2',hero, self.x+(200*count), self.y)
                self.status_hero_team2[name].position = (200*count,0)
                self.add(self.status_hero_team2[name])
                count = count + 1


class StatusLayer(cocos.layer.ColorLayer):

    def __init__(self, name, button, team, hero_key,local_x, local_y, width=200, height=200 ,r=0, b=0, g=0, a=0):
        super().__init__(r,b,g,a, width=width, height=height)
        self.text_hero = cocos.text.Label(name, font_size = 15, bold= True)
        self.text_hp = cocos.text.Label('HP: ', font_size = 10, bold= True)
        self.hp_bar = Bar()
        self.text_mana = cocos.text.Label('MP: ', font_size = 10, bold= True)
        self.events_status = cocos.text.Label('events: ', font_size = 10, bold= True)
        self.mana_bar = Bar(0,0,255,100)
        self.is_event_handler = True
        self.hero_key = hero_key
        self.ac = ApaimaneeMOBAClient()
        self.team = team
        self.button = button
        self.local_x = local_x
        self.local_y = local_y
        self.timer = 0

        self.text_hero.position = (50, 150)
        self.text_hp.position = (20, 120)
        self.hp_bar.position = (45,120)
        self.text_mana.position = (20, 100)
        self.mana_bar.position = (45,100)
        self.events_status.position = (20, 80)
        self.button.set_local(self.local_x+self.x, self.local_y+self.y)
        self.button.position=(5,0)
        self.add(self.text_hero,1)
        self.add(self.text_hp,2)
        self.add(self.text_mana,2)
        self.add(self.button,0)
        self.add(self.hp_bar,1)
        self.add(self.mana_bar,1)
        self.add(self.events_status, 1)

        self.schedule(self.step)
        print(self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key])

    def update_status(self):
        hp = self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key]['current_hp']
        max_hp = self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key]['max_hp']
        mana = self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key]['current_mana']
        max_mana = self.ac.game_logic.game_space['hero_'+ self.team][self.hero_key]['max_mana']
        events_status = self.ac.game_logic.game_space['hero_'+self.team][self.hero_key]['act_status']['action']
        
        self.hp_bar.update(hp,max_hp)
        self.mana_bar.update(mana,max_mana)
        self.text_hp.element.text = 'HP: ' + str(hp)
        self.text_mana.element.text = 'MP: ' + str(mana)
        self.events_status.element.text = 'Events: ' + str(events_status)

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
        self.name = cocos.text.Label(name, font_size = 20, bold= True)
        self.name.position = (55,5)
        self.add(self.name)

        self.img = pyglet.resource.image('sim_monitor/res/newbutton.png')

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
            print(self.hero_key) 
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

        self.img = pyglet.resource.image('sim_monitor/res/show_status.png')
        self.hp_bar = Bar()
        self.mana_bar = Bar(0,0,255,100)
        self.text_team = cocos.text.Label('Team ', font_size = 20, bold= True)
        self.text_name = cocos.text.Label('Name: ', font_size = 20, bold= True)
        self.text_hp = cocos.text.Label('HP: ', font_size = 12, bold= True)
        self.text_mana = cocos.text.Label('MP: ', font_size = 12, bold= True)
        self.text_damage = cocos.text.Label('Damage: ', font_size = 12, bold= True)
        self.text_str = cocos.text.Label('Strength: ', font_size = 12, bold= True)
        self.text_armor = cocos.text.Label('Armor: ', font_size = 12, bold= True)
        self.text_magic = cocos.text.Label('Magic: ', font_size = 12, bold= True)
        self.text_level = cocos.text.Label('Level: ', font_size = 15, bold= True)
        self.text_alive = cocos.text.Label('Alive: ', font_size = 15, bold= True)
        self.text_gold = cocos.text.Label('Coin: ', font_size = 15, bold= True)

        self.text_damage_critical = cocos.text.Label('Damage Critical: ', font_size = 12, bold= True)
        self.text_magic_resis = cocos.text.Label('Magic Resist: ', font_size = 12, bold= True)
        self.text_damage_speed = cocos.text.Label('Damage Speed: ', font_size = 12, bold= True)
        self.text_move_speed = cocos.text.Label('Move Speed: ', font_size = 12, bold= True)
        self.text_skills = cocos.text.Label('Skill: ', font_size = 12, bold= True)
        self.events_status = cocos.text.Label('Events: ', font_size = 12, bold= True)



        self.is_event_handler = True
        self.timer = 0

        self.text_team.position = (100, 700)
        self.text_name.position = (300, 700)
        self.text_hp.position = (250, 660)
        self.hp_bar.position  = (285, 660)
        self.text_mana.position = (450, 660)
        self.mana_bar.position = (485,660)
        self.text_damage.position = (150, 630)
        self.text_str.position = (450, 630)
        self.text_magic.position = (300, 630)
        self.text_armor.position = (600, 630)
        self.text_level.position = (50, 660)
        self.text_gold.position = (50, 550)
        self.events_status.position = (50, 350)
        self.text_alive.position = (600, 550)

        self.text_damage_critical.position = (50, 450)
        self.text_damage_speed.position = (50, 430)
        self.text_magic_resis.position = (50, 410)
        self.text_move_speed.position = (50, 390)
        self.text_skills.position = (50,370)
#       add text        
        self.add(self.text_team,1)
        self.add(self.text_name,1)
        self.add(self.text_hp,1)
        self.add(self.text_mana,1)
        self.add(self.text_damage,1)
        self.add(self.text_str,1)
        self.add(self.text_armor,1)
        self.add(self.text_magic,1)
        self.add(self.text_level,1)
        self.add(self.text_gold,1)
        self.add(self.hp_bar,1)
        self.add(self.mana_bar,1)
        self.add(self.events_status,1)

        self.add(self.text_damage_critical,1)
        self.add(self.text_magic_resis,1)
        self.add(self.text_damage_speed,1)
        self.add(self.text_move_speed,1)
        self.add(self.text_skills,1)
        self.add(self.text_alive,1)

        self.schedule(self.step)

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()


    def update_status(self):
        if status.hero_key != None:
            if status.hero_key in self.game_space['hero_team1']:
                name = self.game_space['hero_team1'][status.hero_key]['name']
                hp = self.game_space['hero_team1'][status.hero_key]['current_hp']
                max_hp = self.game_space['hero_team1'][status.hero_key]['max_hp'] 
                mana = self.game_space['hero_team1'][status.hero_key]['current_mana']
                max_mana = self.game_space['hero_team1'][status.hero_key]['max_mana']
                damage = self.game_space['hero_team1'][status.hero_key]['damage']
                strength  = self.game_space['hero_team1'][status.hero_key]['str']
                armor = self.game_space['hero_team1'][status.hero_key]['armor']
                magic = self.game_space['hero_team1'][status.hero_key]['magic']
                level = self.game_space['hero_team1'][status.hero_key]['current_exp']
                gold = self.game_space['hero_team1'][status.hero_key]['gold']
                alive = self.game_space['hero_team1'][status.hero_key]['alive']

                damage_critical = self.game_space['hero_team1'][status.hero_key]['damage_critical']
                magic_resis = self.game_space['hero_team1'][status.hero_key]['magic_resis']
                damage_speed = self.game_space['hero_team1'][status.hero_key]['damage_speed']
                move_speed = self.game_space['hero_team1'][status.hero_key]['move_speed']
                events_status = self.game_space['hero_team1'][status.hero_key]['act_status']['action']


                if self.game_space['hero_team1'][status.hero_key]['skills'][0]:
                    skills = self.game_space['hero_team1'][status.hero_key]['skills'][0]['name']
                if self.game_space['hero_team1'][status.hero_key]['skills'][1]:
                    skills = self.game_space['hero_team1'][status.hero_key]['skills'][1]['name']
                if self.game_space['hero_team1'][status.hero_key]['skills'][2]:
                    skills = self.game_space['hero_team1'][status.hero_key]['skills'][2]['name']
                if self.game_space['hero_team1'][status.hero_key]['skills'][3]:
                    skills = self.game_space['hero_team1'][status.hero_key]['skills'][3]['name']

                self.text_team.element.text = 'Team 1'
                self.text_name.element.text = 'Name: ' + str(name)
                self.text_hp.element.text = 'HP: ' + str(hp) + '/' + str(max_hp)
                self.text_mana.element.text = 'MP: ' + str(mana) + '/' + str(max_mana)
                self.text_damage.element.text = 'Damage: ' + str(damage)
                self.text_str.element.text = 'Strength: ' + str(strength)
                self.text_armor.element.text = 'Armor: ' + str(armor)
                self.text_magic.element.text  = 'Magic: ' + str(magic)
                self.text_level.element.text = 'Level: ' + str(level)
                self.text_gold.element.text = 'Coin: ' + str(gold)
                self.events_status.element.text = 'Events: ' + str(events_status)
                self.text_damage_critical.element.text = 'Damage Critical: ' + str(damage_critical)
                self.text_magic_resis.element.text = 'Magic Resist: ' + str(magic_resis)
                self.text_damage_speed.element.text = 'Damage Speed: ' + str(damage_speed)
                self.text_move_speed.element.text = 'Move Speed: ' + str(move_speed)
                self.text_skills.element.text = 'Skill: ' + str(skills)
                self.text_alive.element.text = 'Alive: ' + str(alive)
                self.hp_bar.update(hp,max_hp)
                self.mana_bar.update(mana,max_mana)
            
            else: 
                name = self.game_space['hero_team2'][status.hero_key]['name']
                hp = self.game_space['hero_team2'][status.hero_key]['current_hp']
                max_hp = self.game_space['hero_team2'][status.hero_key]['max_hp'] 
                mana = self.game_space['hero_team2'][status.hero_key]['current_mana']
                max_mana = self.game_space['hero_team2'][status.hero_key]['max_mana']
                damage = self.game_space['hero_team2'][status.hero_key]['damage']
                strength  = self.game_space['hero_team2'][status.hero_key]['str']
                armor = self.game_space['hero_team2'][status.hero_key]['armor']
                magic = self.game_space['hero_team2'][status.hero_key]['magic']
                level = self.game_space['hero_team2'][status.hero_key]['current_exp']
                gold = self.game_space['hero_team2'][status.hero_key]['gold']
                alive = self.game_space['hero_team2'][status.hero_key]['alive']
                damage_critical = self.game_space['hero_team2'][status.hero_key]['damage_critical']
                magic_resis = self.game_space['hero_team2'][status.hero_key]['magic_resis']
                damage_speed = self.game_space['hero_team2'][status.hero_key]['damage_speed']
                move_speed = self.game_space['hero_team2'][status.hero_key]['move_speed']

                events_status = self.game_space['hero_team2'][status.hero_key]['act_status']['action']
                if self.game_space['hero_team2'][status.hero_key]['skills'][0]:
                    skills = self.game_space['hero_team2'][status.hero_key]['skills'][0]['name']
                if self.game_space['hero_team2'][status.hero_key]['skills'][1]:
                    skills = self.game_space['hero_team2'][status.hero_key]['skills'][1]['name']
                if self.game_space['hero_team2'][status.hero_key]['skills'][2]:
                    skills = self.game_space['hero_team2'][status.hero_key]['skills'][2]['name']
                if self.game_space['hero_team2'][status.hero_key]['skills'][3]:
                    skills = self.game_space['hero_team2'][status.hero_key]['skills'][3]['name']

                self.text_team.element.text = 'Team 2'
                self.text_name.element.text = 'Name: ' + str(name)
                self.text_hp.element.text = 'HP: ' + str(hp) + '/' + str(max_hp)
                self.text_mana.element.text = 'MP: ' + str(mana) + '/' + str(max_mana)
                self.text_damage.element.text = 'Damage: ' + str(damage)
                self.text_str.element.text = 'Strength: ' + str(strength)
                self.text_armor.element.text = 'Armor: ' + str(armor)
                self.text_magic.element.text  = 'Magic: ' + str(magic)
                self.text_level.element.text = 'Level: ' + str(level)
                self.text_gold.element.text = 'Coin: ' + str(gold)
                self.events_status.element.text = 'Events: ' + str(events_status)

                self.text_damage_critical.element.text = 'Damage Critical: ' + str(damage_critical)
                self.text_magic_resis.element.text = 'Magic Resist: ' + str(magic_resis)
                self.text_damage_speed.element.text = 'Damage Speed: ' + str(damage_speed)
                self.text_move_speed.element.text = 'Move Speed: ' + str(move_speed)
                self.text_skills.element.text = 'Skill: ' + str(skills)
                self.text_alive.element.text = 'Alive: ' + str(alive)
                self.hp_bar.update(hp,max_hp)
                self.mana_bar.update(mana,max_mana)


    def step(self, dt):
        self.game_space = self.ac.game_logic.game_space
        self.timer += dt
        if self.timer > 0.01:
            self.timer = 0
            self.update_status()
