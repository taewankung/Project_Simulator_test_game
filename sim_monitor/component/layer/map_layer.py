#
# cocos2d
# http://python.cocos2d.org
#

from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
import cocos
import pyglet
from pyglet.gl import *
colors =["red","orange","green","blue","yellow"]
class BackgroundMap(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.img =pyglet.resource.image('sim_monitor/res/Labelled_Map.png')
    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0,0)
        glPopMatrix()

class MapLayer(cocos.layer.Layer):
    def __init__(self):
        super(MapLayer,self).__init__()
        self.bg = BackgroundMap()
        self.add(self.bg)
        self.is_event_handler = True
        self.sprite_hero_team1 = [cocos.sprite.Sprite('sim_monitor/res/star_%s.png' % color) for color in colors]
        self.sprite_hero_team2 =[cocos.sprite.Sprite('sim_monitor/res/pentagon_%s.png'%color) for color in colors]
        self.ac = None
        self.sprite_tower_team1 = {
                                   't1_tower_top_level1':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_top_level2':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_top_level3':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_mid_level1':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_mid_level2':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_mid_level3':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_bot_level1':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_bot_level2':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_bot_level3':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_base_left' :cocos.sprite.Sprite('sim_monitor/res/sqr_red.png'),
                                   't1_tower_base_right':cocos.sprite.Sprite('sim_monitor/res/sqr_red.png')
                                  }

        self.sprite_tower_team2 = {
                                   't2_tower_top_level1':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_top_level2':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_top_level3':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_mid_level1':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_mid_level2':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_mid_level3':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_bot_level1':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_bot_level2':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_bot_level3':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_base_left' :cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png'),
                                   't2_tower_base_right':cocos.sprite.Sprite('sim_monitor/res/sqr_blue.png')
                                  }

        # add Hero symbol

        for hero_team1 in self.sprite_hero_team1:
            hero_team1.scale = 0.10
            self.add(hero_team1)

        for hero_team2 in self.sprite_hero_team2:
            hero_team2.scale = 0.10
            self.add(hero_team2)

        # add tower symbol
        for tw in self.sprite_tower_team1 :
            self.sprite_tower_team1[tw].scale = 0.5
            self.add(self.sprite_tower_team1[tw])

        for tw in self.sprite_tower_team2 :
            self.sprite_tower_team2[tw].scale = 0.5
            self.add(self.sprite_tower_team2[tw])
        self.posx = 0
        self.posy = 850
        self.text = cocos.text.Label('No mouse events yet', font_size=30, x=self.posx, y=self.posy )
        self.add(self.text)
    '''def on_mouse_motion (self, x, y, dx, dy):
        """Called when the mouse moves over the app window with no button pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
        last call.
        """
        self.update_text (x, y)'''

    def on_mouse_press (self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed
        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
        (values like 'SHIFT', 'OPTION', 'ALT')
        """
        self.posx, self.posy = cocos.director.director.get_virtual_coordinates (x, y)
        self.update_text (x,y)

    def update_text (self, x, y):
        text = 'Mouse @ %d,%d' % (x, y)
        self.text.element.text = text
        #self.text.element.x = self.posx
        #self.text.element.y = self.posy

    def set_with_ac(self, ac):
        self.ac = ac
        for tw in ac.game_logic.game_space["tower_team1"]:
            pos = (ac.game_logic.game_space["tower_team1"][tw]['pos_x'],
                    ac.game_logic.game_space["tower_team1"][tw]['pos_y'])
#            print( ac.game_logic.game_space["tower_team1"][tw]["name"])
#            print(pos)
            self.set_position(ac.game_logic.game_space["tower_team1"][tw]["name"],pos)
        for tw in ac.game_logic.game_space["tower_team2"]:
            pos = (ac.game_logic.game_space["tower_team2"][tw]['pos_x'],
                    ac.game_logic.game_space["tower_team2"][tw]['pos_y'])
#            print( ac.game_logic.game_space["tower_team2"][tw]["name"])
#            print(pos)
            self.set_position(ac.game_logic.game_space["tower_team2"][tw]["name"],pos)
#        self.ac.game_client.game.move_hero(0,0);
        if len(ac.game_logic.game_space["creep_team1"]) != 0 :
            print(">X<")

    def set_position(self,name , position):
        if name in self.sprite_tower_team1:
            self.sprite_tower_team1[name].position = position
        elif name in self.sprite_tower_team2:

            self.sprite_tower_team2[name].position = position
        else:
            #print(self.ac.game_logic.game_space["tower_team2"])
            print("have not in game_space {0}".format(name))

    

'''    def setBase(self,team_name = 'team1' ,position = (0,0)):
        #team_name have blue and red
        if team_name.lower() in ['team1','team2']:
            self.sprite_base[team_name].position = position

    def setTower(position_tower= 'mid',team= 'team1',level_tower ='lvl0',position = (0,0)):
        if team == 'team2':
            tower_seter = self.sprite_tower_team2[position_tower][level_tower]
            tower_seter.position = position
        else:
            tower_seter = self.sprite_tower_team1[position_tower][level_tower]
            tower_seter.position = position

    def get_tower(team = 'team1'):
        if team == 'team1':
            return self.sprite_tower_team1
        elif team == 'team2':
            return self.sprite_tower_team2

    def get_base():
        return self.sprite_base

    def get_hero(team='team1'):
        if team == 'team1':
            return self.sprite_hero_team1
        elif team == 'team2':
            return self.sprite_hero_team2'''
