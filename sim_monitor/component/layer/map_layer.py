#
# cocos2d
# http://python.cocos2d.org
#

from __future__ import division, print_function, unicode_literals
import pyglet
import cocos

# This code is so you can run the samples without installing the package
import sys
import os
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from pyglet.gl import *
from pyglet.window import key

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#
colors = ["red", "orange", "green", "blue", "yellow"]


class BackgroundMap(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        #  self.img = pyglet.resource.image('sim_monitor/res/Labelled_Map.png')

    #  def draw(self):
        #  glPushMatrix()
        #  self.transform()
        #  self.img.blit(0, 0)
        #  glPopMatrix()


class MapLayer(cocos.layer.Layer):

    def __init__(self, model):
        super(MapLayer, self).__init__()
        self.model = model
#        self.model.push_handlers(self.update_map)
        self.bg = BackgroundMap()
        self.add(self.bg)
        self.is_event_handler = True
        self.count_hero_team1 = 0
        self.count_hero_team2 = 0
        self.sprite_hero_team1 = [cocos.sprite.Sprite('sim_monitor/res/star_%s.png' % color) for color in colors]
        self.hero_team1 = {}
        self.hero_team2 = {}
        self.sprite_hero_team2 = [cocos.sprite.Sprite('sim_monitor/res/pentagon_%s.png' % color) for color in colors]
        self.ac = None
        self.sprite_creep_team1 = {}
        self.sprite_creep_team2 = {}
        self.sprite_tower_team1 = {'t1_tower_top_level1': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_top_level2': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_top_level3': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_mid_level1': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_mid_level2': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_mid_level3': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_bot_level1': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_bot_level2': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_bot_level3': cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_base_left':  cocos.sprite.Sprite('sim_monitor/res/tower-red.png'),
                                   't1_tower_base_right': cocos.sprite.Sprite('sim_monitor/res/tower-red.png')}

        self.sprite_tower_team2 = {'t2_tower_top_level1': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_top_level2': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_top_level3': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_mid_level1': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_mid_level2': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_mid_level3': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_bot_level1': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_bot_level2': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_bot_level3': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_base_left':  cocos.sprite.Sprite('sim_monitor/res/tower-blue.png'),
                                   't2_tower_base_right': cocos.sprite.Sprite('sim_monitor/res/tower-blue.png')}
        self.timer = 0
        # add Hero symbol

        #  for hero_team1 in self.sprite_hero_team1:
            #  hero_team1.scale = 0.30
            #  self.add(hero_team1)

        #  for hero_team2 in self.sprite_hero_team2:
            #  hero_team2.scale = 0.30
            #  self.add(hero_team2)

        # add tower symbol
        for tw in self.sprite_tower_team1:
            self.sprite_tower_team1[tw].scale = 0.5
            self.add(self.sprite_tower_team1[tw])

        for tw in self.sprite_tower_team2:
            self.sprite_tower_team2[tw].scale = 0.5
            self.add(self.sprite_tower_team2[tw])
        self.posx = 0
        self.posy = 850
        self.text = cocos.text.Label('No mouse events yet',
                                     font_size=30,
                                     x=self.posx, y=self.posy)
        self.add(self.text)

    def on_mouse_press(self, x, y, buttons, modifiers):

        self.posx,
        self.posy = cocos.director.director.get_virtual_coordinates(x, y)

        self.update_text(x, y)

    def on_key_press(self,k,m):
        if k == key.NUM_MULTIPLY:
            self.ac.game_client.game.stop()
        pass


    def update_text(self, x, y):
        text = 'Mouse @ %d,%d' % (x, y)
        self.text.element.text = text

    def set_with_ac(self, ac):
        self.ac = ac
        for tw in ac.game_logic.game_space["tower_team1"]:
            pos = (ac.game_logic.game_space["tower_team1"][tw]['pos_x'],
                   ac.game_logic.game_space["tower_team1"][tw]['pos_y'])
            self.set_position_tower(ac.game_logic.game_space["tower_team1"][tw]["name"], pos)
        for tw in ac.game_logic.game_space["tower_team2"]:
            pos = (ac.game_logic.game_space["tower_team2"][tw]['pos_x'],
                   ac.game_logic.game_space["tower_team2"][tw]['pos_y'])
            self.set_position_tower(ac.game_logic.game_space["tower_team2"][tw]["name"], pos)
        for hero in ac.game_logic.game_space["hero_team1"]:
            pos = ( ac.game_logic.game_space["hero_team1"][hero]['pos_x'],
                     ac.game_logic.game_space["hero_team1"][hero]['pos_y'])
        self.schedule(self.step)

    def set_position_tower(self, name, position):
        if name in self.sprite_tower_team1:
            self.sprite_tower_team1[name].position = position
        elif name in self.sprite_tower_team2:
            self.sprite_tower_team2[name].position = position
        else:
            print("have not in game_space {0}".format(name))

    def set_position(self, sprite, pos_x, pos_y):
        position = (pos_x, pos_y)
        sprite.position = position

    def step(self, dt):
        self.timer += dt
        if self.timer > 0.01:
            self.timer = 0
            if self.ac is not None:
                game_space = self.ac.game_logic.game_space
                for hero in game_space["hero_team1"]:
                    if hero not in self.hero_team1:
                        self.count_hero_team1 += 1
                        self.hero_team1[hero] = self.sprite_hero_team1[self.count_hero_team1-1]
                        self.hero_team1[hero].scale = 0.3
                        pos = (game_space["hero_team1"][hero]['pos_x'],
                           game_space["hero_team1"][hero]['pos_y'])
                        self.hero_team1[hero].position = pos
                        self.add(self.hero_team1[hero],2)
                for hero in game_space["hero_team2"]:
                    if hero not in self.hero_team2:
                        self.count_hero_team2 += 1
                        self.hero_team2[hero] = self.sprite_hero_team2[self.count_hero_team2-1]
                        self.hero_team2[hero].scale = 0.3
                        pos = (game_space["hero_team2"][hero]['pos_x'],
                           game_space["hero_team2"][hero]['pos_y'])
                        self.hero_team2[hero].position = pos
                        self.add(self.hero_team2[hero],2)

                for tw in game_space["tower_team1"]:
                    pos = (game_space["tower_team1"][tw]['pos_x'],
                           game_space["tower_team1"][tw]['pos_y'])
                    self.set_position_tower(game_space["tower_team1"][tw]["name"], pos)
                for tw in game_space["tower_team2"]:
                    pos = (game_space["tower_team2"][tw]['pos_x'],
                           game_space["tower_team2"][tw]['pos_y'])
                    self.set_position_tower(game_space["tower_team2"][tw]["name"], pos)
#//////////////////////////////Creep display/////////////////////////////////////////////
#//////////////////////////////Creep_team1///////////////////////////////////////////////
                for creep in game_space["creep_team1"]:
                    if game_space["creep_team1"][creep]["alive"]:
                        if creep not in self.sprite_creep_team1:
                            self.sprite_creep_team1[creep] = cocos.sprite.Sprite('sim_monitor/res/square_red.png')
                            self.sprite_creep_team1[creep].scale = 0.1
                            self.add(self.sprite_creep_team1[creep])
                        self.set_position(
                                        self.sprite_creep_team1[creep],
                                        game_space["creep_team1"][creep]['pos_x'],
                                        game_space["creep_team1"][creep]['pos_y'])
                    else:
                        if creep in self.sprite_creep_team1:
                            #self.sprite_creep_team1[creep].visible = False
                            self.remove(self.sprite_creep_team1[creep])
                            #self.sprite_creep_team1.pop(creep)
                new_list =[]
                for s_creep in self.sprite_creep_team1:
                            #self.sprite_creep_team2[creep].visible = False
                    if s_creep not in  game_space['creep_team1']:
                        self.remove(self.sprite_creep_team1[s_creep])
                        new_list.append(s_creep)
                for creep_id in new_list:
                    self.sprite_creep_team1.pop(creep_id)
                        #self.sprite_creep_team2.pop(creep)
#///////////////////////////////Creep_team2/////////////////////////////////////////////
                for creep in game_space["creep_team2"]:
                    if game_space["creep_team2"][creep]["alive"]:
                        if creep not in self.sprite_creep_team2:
                            self.sprite_creep_team2[creep] = cocos.sprite.Sprite('sim_monitor/res/square_blue.png')
                            self.sprite_creep_team2[creep].scale = 0.1
                            self.add(self.sprite_creep_team2[creep])
                        self.set_position(
                                        self.sprite_creep_team2[creep],
                                        game_space["creep_team2"][creep]['pos_x'],
                                        game_space["creep_team2"][creep]['pos_y'])
                    else:
                        if creep in self.sprite_creep_team2:
                            self.remove(self.sprite_creep_team2[s_creep])
                new_list =[]
                for s_creep in self.sprite_creep_team2:
                    if s_creep not in  game_space['creep_team2']:
                        self.remove(self.sprite_creep_team2[s_creep])
                        new_list.append(s_creep)
                for creep_id in new_list:
                    self.sprite_creep_team2.pop(creep_id)
                        #self.sprite_creep_team2.pop(s_creep)
#///////////////////////////////////Hero_display////////////////////////////////////////////////
#//////////////////////////////////Hero_team1//////////////////////////////////////////////////
                for hero_id in game_space["hero_team1"]:
                    if game_space["hero_team1"][hero_id]["alive"]:
                        self.hero_team1[hero_id].visible = True
                        self.set_position(
                                        self.hero_team1[hero_id],
                                        game_space["hero_team1"][hero_id]['pos_x'],
                                        game_space["hero_team1"][hero_id]['pos_y'])
                    else:
                        self.hero_team1[hero_id].visible = False

#////////////////////////////////Hero_team2///////////////////////////////////////////////////
                for hero_id in game_space["hero_team2"]:
                    if game_space["hero_team2"][hero_id]["alive"]:
                        self.hero_team2[hero_id].visible = True
                        self.set_position(
                                        self.hero_team2[hero_id],
                                        game_space["hero_team2"][hero_id]['pos_x'],
                                        game_space["hero_team2"][hero_id]['pos_y'])
                    else:
                        self.hero_team2[hero_id].visible = False
#///////////////////////////////////Tower_distplay////////////////////////////////////////////
#///////////////////////////////////Tower_team1///////////////////////////////////////////////
                for tw_id in game_space["tower_team1"]:
                    tw_name = game_space["tower_team1"][tw_id]['name']
                    if game_space["tower_team1"][tw_id]["alive"]:
                        self.sprite_tower_team1[tw_name].visible = True
                    else:
                        self.sprite_tower_team1[tw_name].visible = False
#///////////////////////////////////Tower_team2///////////////////////////////////////////////
                for tw_id in game_space["tower_team2"]:
                    tw_name = game_space["tower_team2"][tw_id]['name']
                    if game_space["tower_team2"][tw_id]["alive"]:
                        self.sprite_tower_team2[tw_name].visible = True
                    else:
                        self.sprite_tower_team2[tw_name].visible = False
