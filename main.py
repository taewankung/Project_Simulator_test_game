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

if __name__ == "__main__":
    global send_initial
    #  parser = OptionParser()
    #  parser.add_option("-f", "--file", dest="filename",
                  #  help="write report to FILE", metavar="FILE")
    #  parser.add_option("-q", "--quiet",
                  #  action="store_false", dest="verbose", default=True,
                  #  help="don't print status messages to stdout")

#    (options, args) = parser.parse_args()
    #  parser = argparse.ArgumentParser(prog='Sim_map',
                                     #  description='Simulation of MOBA game'
                                    #  )
    #  parser.add_argument('--test', nargs='?', const='test',
                              #  default='test',
                              #  help='ApaimaneeMOBA client_id')
    #  args=parser.parse_args()
    #  print(args)
    send_initial = False
    start_time = None
    connector = Connector()
    connector.start()
    logger.info("Hello")


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
    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
