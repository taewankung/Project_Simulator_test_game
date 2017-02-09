import cocos
import datetime
import time
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.sim_client.connection import initial_game
from sim_monitor.component.scene.main_scene import MainScene
from threading import Thread
import asyncio

class ConnectionLayer(cocos.layer.Layer):
    def __init__(self,model):
        super().__init__()
        self.model = model
        self.model.push_handlers( self.check_connecting
                                )
        self.label= cocos.text.Label("",
                                 font_size = 32,
                                 anchor_x='center',
                                 anchor_y='center')
        self.label.position = 500,500
        self.add(self.label)
        self.model.start()

    def check_connecting(self):
        cocos.director.director.replace(MainScene(self.model))
        return True
