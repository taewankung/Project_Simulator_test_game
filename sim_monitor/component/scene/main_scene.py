
import cocos

from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.component.layer.map_layer import MapLayer
from sim_monitor.component.layer.status_layer import StatusLayer
from sim_monitor.component.layer.status_layer import BackgroundSim

class MainScene(cocos.scene.Scene):
    def __init__(self, model):
        super().__init__()
        self.ac = ApaimaneeMOBAClient()
        self.model = model
        self.map_layer = MapLayer(model)
        self.map_layer.scale = 0.5
        #self.background_sim = BackgroundSim()
        self.background = cocos.layer.ColorLayer(255, 255, 255, 100, width=1000, height=1000) #colorbackmap
        self.background.scale = 0.5

        self.team1_stat_bg = cocos.layer.ColorLayer(255, 0, 255, 100, width=1000, height=1000)
        self.team1_stat_bg.scale_y = 0.2
        self.team1_stat_bg.transform_anchor = 0, 1100

        self.status_layer1 = StatusLayer()
        self.status_layer1.postition= (0,0)

        self.team2_stat_bg = cocos.layer.ColorLayer(255, 0, 0, 100, width=1000, height=1000)
        self.team2_stat_bg.scale_y = 0.2
        self.team2_stat_bg.transform_anchor = 0, 0


        self.status_layer = StatusLayer()
        self.status_layer.posititon=(400,0)

#        set initial position
        self.map_layer.position=(-200,0)
        self.background.position=(-200,0)
#        add to main scene
        self.add(self.background)
        #self.add(self.background_sim)
        self.add(self.map_layer, 1)
        self.add(self.team1_stat_bg)
        self.add(self.status_layer1,1)
        self.add(self.team2_stat_bg)
        self.add(self.status_layer, 1)
        self.map_layer.set_with_ac(self.ac)
        self.status_layer.load_hero()


