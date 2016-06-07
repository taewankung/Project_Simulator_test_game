from sim_monitor.component.map_layer  import MapLayer
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.sim_client.connection import initial_game

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
    connection = False

    # connect to server
    while not connection:
        if start_time != None:
            ac = ApaimaneeMOBAClient()
            if ac.game_logic.status == 'play':
                print("//////////////////PLAY///////////////////")
                connection = True
            diff_time = datetime.datetime.now() - start_time
            time.sleep(1)
            print('wait for play singnal', diff_time.seconds)
            if diff_time.seconds % 20 == 0:
                if not send_initial:
                    ac.game_client.game.initial()
                    send_initial = True
            else:
                send_initial = False
            if diff_time > datetime.timedelta(minutes=2):
                print('time out')
                ac.disconnect()
        else:
            try:
                initial_game()
            except Exception as e:
                print('Initial Fail:', e)
            start_time = datetime.datetime.now()

    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(resizable=True,width = 1000, height=900)
    # We create a new layer, an instance of HelloWorld
    map_layer = MapLayer()
    background = cocos.layer.ColorLayer(255,255,255,100)
    team1_stat_bg = cocos.layer.ColorLayer(255,0,255,100)
    team2_stat_bg = cocos.layer.ColorLayer(255,0,0,100)
    team1_stat_bg.scale_y =0.2
    team1_stat_bg.transform_anchor = 0,900
    team2_stat_bg.scale_y =0.2
    team2_stat_bg.transform_anchor = 0, 0
    background.scale = 0.5
    map_layer.scale = 0.5
    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(background)
    main_scene.add(map_layer,1)
    main_scene.add(team1_stat_bg)
    main_scene.add(team2_stat_bg)
    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
