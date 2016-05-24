from component.map_layer  import MapLayer

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cocos

if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(resizable=True,width = 1000,height=900)

    # We create a new layer, an instance of HelloWorld
    map_layer = MapLayer()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(map_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
