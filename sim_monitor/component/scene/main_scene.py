
import cocos
import pyglet
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.component.layer.map_layer import MapLayer
from sim_monitor.component.layer.status_layer import StatusLayer
from sim_monitor.component.layer.status_layer import StatusBackground
from sim_monitor.component.layer.status_layer import DisplayStatusLayer
from pyglet.gl import *


class BackgroundSim(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.img = pyglet.resource.image('sim_monitor/res/background.png')

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0,60)
        #move_to(position)
        glPopMatrix()


class MainScene(cocos.scene.Scene):
    def __init__(self, model):
        super().__init__()
        self.ac = ApaimaneeMOBAClient()
        self.model = model
        self.map_layer = MapLayer(model)
        self.map_layer.scale = 0.5


        self.background_sim = BackgroundSim()
        self.background = cocos.layer.ColorLayer(255, 255, 255, 100, width=1000, height=1000) #colorbackmap
        self.background.scale = 0.5

        self.status_team1 = StatusBackground(255,0,255,100, 'Team1',width=1000, height=200 )
        self.status_team1.position = (50,850)

        self.status_team2 = StatusBackground(255,0,0,100, 'Team2', width=1000, height=200)
        self.status_team2.position = (50,95)

#       set display status hero

        self.display_status = DisplayStatusLayer(255, 255, 255, 100)
        self.display_status.position = (1090,150)
#        set initial position
        self.map_layer.position=(-200,50)
        self.background.position=(-200,50)
#        add to main scene
        self.add(self.background)

        self.add(self.background_sim,1)
        self.add(self.map_layer, 1)
        self.add(self.status_team1,1)
        self.add(self.status_team2,1)
        self.map_layer.set_with_ac(self.ac)
        self.status_team1.load_hero()
        self.status_team2.load_hero()
        self.add(self.display_status, 1)
