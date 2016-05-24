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

import cocos
colors =['blue','red','yellow','green','orange']
lvl_tower = ['lvl1','lvl2','lvl3']
class MapLayer(cocos.layer.Layer):
    def __init__(self):
        super(MapLayer,self).__init__()
        self.sprite_hero_team1 = [cocos.sprite.Sprite('res/star_%s.png' % color) for color in colors]
        self.sprite_hero_team2 =[cocos.sprite.Sprite('res/pentagon_%s.png'%color) for color in colors]

        self.sprite_tower_team1 = {
                                   'top': {
                                            'lvl1':cocos.sprite.Sprite('res/sqr_red.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_red.png'),
                                            'lvl3':cocos.sprite.Sprite('res/sqr_red.png')
                                          },
                                   'mid': {
                                            'lvl1':cocos.sprite.Sprite('res/sqr_red.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_red.png'),
                                            'lvl3':cocos.sprite.Sprite('res/sqr_red.png')
                                          },
                                   'btm': {
                                            'lvl1':cocos.sprite.Sprite('res/sqr_red.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_red.png'),
                                            'lvl3':cocos.sprite.Sprite('res/sqr_red.png')
                                          },
                                   'home':{
                                            'lvl1':cocos.sprite.Sprite('res/sqr_red.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_red.png')
                                          }
                                  }

        self.sprite_tower_team2 = {
                                   'top': {
                                            'lvl1':cocos.sprite.Sprite('res/sqr_blue.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_blue.png'),
                                            'lvl3':cocos.sprite.Sprite('res/sqr_blue.png')
                                          },
                                   'mid': {
                                            'lvl1':cocos.sprite.Sprite('res/sqr_blue.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_blue.png'),
                                            'lvl3':cocos.sprite.Sprite('res/sqr_blue.png')
                                          },
                                   'btm': {
                                            'lvl1':cocos.sprite.Sprite('res/sqr_blue.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_blue.png'),
                                            'lvl3':cocos.sprite.Sprite('res/sqr_blue.png')
                                          },
                                   'home':{
                                            'lvl1':cocos.sprite.Sprite('res/sqr_blue.png'),
                                            'lvl2':cocos.sprite.Sprite('res/sqr_blue.png')
                                          }
                                  }
        self.sprite_base = { 'team1': cocos.sprite.Sprite('res/circle_blue.png'),
                             'team2' : cocos.sprite.Sprite('res/circle_red.png')
                           }

        # add Hero symbol

        for hero_team1 in self.sprite_hero_team1:
            self.add(hero_team1)

        for hero_team2 in self.sprite_hero_team2:
            self.add(hero_team2)

        # add tower symbol
        for lvl in lvl_tower:
            self.add(self.sprite_tower_team1["top"][lvl])
            self.add(self.sprite_tower_team1["mid"][lvl])
            self.add(self.sprite_tower_team1["btm"][lvl])
            self.add(self.sprite_tower_team2["top"][lvl])
            self.add(self.sprite_tower_team2["top"][lvl])
            self.add(self.sprite_tower_team2["btm"][lvl])

        # add base symbol sprite_base[0] = 'blue',sprite_base[1] = 'red'
        for base in self.sprite_base:
            self.add(self.sprite_base[base])

    def setBase(self,team_name = 'team1' ,position = (0,0)):
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
            return self.sprite_hero_team2
