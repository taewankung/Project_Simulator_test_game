import sys
import os
import time
import datetime
import threading
import pyglet
import cocos

from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.component.layer.connection_layer import ConnectionLayer
from sim_monitor.model.gamemodel import GameModel
from sim_monitor.controller.gamectrl import GameCtrl
from sim_monitor.model.status import status
from pyglet.gl import *


class BackgroundLoad(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.img = pyglet.resource.image('sim_monitor/res/background.png')

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0,60)
        #move_to(position)
        glPopMatrix()

class ConnectionScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.game_model = GameModel()
        self.background_load = BackgroundLoad()
        self.game_ctrl = GameCtrl(self.game_model)
        self.game_model.set_controller(self.game_ctrl)
        self.view = ConnectionLayer(self.game_model)
        self.add(self.game_ctrl,z=1, name="controller")
        self.add(self.view,z=2,name="view")

        self.add(self.background_load, 1)

