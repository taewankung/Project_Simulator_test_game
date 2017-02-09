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
import logging
import logging.config
from threading import Thread
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import argparse
#from optparse import OptionParser

import cocos

from cocos.director import director
logger = logging.getLogger('sim_map')
import subprocess
from multiprocessing import Process

class RunGUI(Process):
    def __init__(self):
        super().__init__()
        process = subprocess.Popen('python3 '+os.path.expanduser("~")+'/projects/sim_map/run_gui.py',shell=True)
        #  print(os.path.dirname(__file__))
        #  self.cmd = ['python3',os.path.expanduser("~")+'/projects/sim_map/run_gui.py']

    #  def run(self):
        #  process = subprocess.call(self.cmd)

if __name__ == "__main__":
    global send_initial
    send_initial = False
    start_time = None
    connector = Connector()
    connector.start()

    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(width = 1920, height=1080)
    cocos.director.director.window.set_fullscreen(False)
    x,y = cocos.director.director.get_window_size()
    # We create a new layer, an instance of HelloWorld
    # A scene that contains the layer hello_layer
    first_scene = ConnectionScene()
    # And now, start the application, starting with main_scene
    cocos.director.director.run(first_scene)
    connector.disconnect()
    print('exit_game')
    rungui =RunGUI()
#    rungui.join()
    #  rungui.start()
    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
