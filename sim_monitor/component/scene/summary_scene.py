
import cocos
import pyglet
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
from sim_monitor.component.layer.summary_board import HeroLayer
from sim_monitor.component.layer.summary_board import SummaryBackground
from sim_monitor.component.layer.summary_board import DisplaySummaryLayer
from sim_monitor.component.layer.summary_board import Button
from pyglet.gl import *

class SummaryScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.ac = ApaimaneeMOBAClient()
        self.summary_team1 = SummaryBackground(255,0,255,100, 'Team1',width=900, height=800 )
        self.summary_team1.position = (20,150)
        self.summary_team2 = SummaryBackground(255,0,0,100, 'Team2', width=900, height=800)
        self.summary_team2.position = (1000,150)
        self.text_result = cocos.text.Label('Result: {0}'.format(self.ac.game_logic.end_message), font_size = 25)
        self.text_result.position = (810,980)
        self.button = Button(255,0,0,1,name='Quit')

#       set display status hero
        self.display_summary = DisplaySummaryLayer(255, 255, 255, 100)
        self.display_summary.position = (1090,150)
        self.button.position = (850,75)
        self.button.set_local(850,75)

        self.add(self.summary_team1,1)
        self.add(self.summary_team2,1)
        self.add(self.text_result,1)
        self.add(self.button,1)
        self.summary_team1.load_hero()
        self.summary_team2.load_hero()
#        self.add(self.display_summary, 1)
