from sim_monitor.component.layer.map_layer  import MapLayer
from sim_monitor.component.scene.connection_scene import ConnectionScene
from sim_monitor.model.gamemodel import GameModel
from sim_monitor.controller.gamectrl import GameCtrl
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.sim_client.connection import initial_game
from sim_monitor.controller.connector import Connector
import sys
import os
import time
import datetime
from threading import Thread
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cocos


if __name__ == "__main__":
    global send_initial
    send_initial = False
    start_time = None
    connector = Connector()
    connector.start()
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(resizable=True,width = 1000, height=1000)
    # We create a new layer, an instance of HelloWorld
    # A scene that contains the layer hello_layer
    first_scene = ConnectionScene()
    # And now, start the application, starting with main_scene
    cocos.director.director.run(first_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
