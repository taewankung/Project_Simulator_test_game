from __future__ import division, print_function, unicode_literals

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from cocos.layer import *
from cocos.text import *
from cocos.actions import *

import pyglet
from pyglet.gl import *

from SimMap import MapLayer

class StatusHeroLayer(Layer):
    def __init__(self,map_layer):
        super(StatusHeroLayer,self).__init__()
        self.map_game = map_layer
        self.label = 
    pass
