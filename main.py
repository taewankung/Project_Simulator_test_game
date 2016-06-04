from sim_monitor.component.map_layer  import MapLayer
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.sim_client.connection import loading_scene

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cocos
from sim_client.connection import loading_scene

if __name__ == "__main__":
    # connect to server
    con = {}
    loading_scene()
    ac = ApaimaneeMOBAClient('test_client_id')
    ac.game_client.game.move_hero(0,0)
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(resizable=True,width = 1000, height=900)

    # We create a new layer, an instance of HelloWorld
    map_layer = MapLayer()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(map_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
