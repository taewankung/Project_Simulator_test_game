from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
#from kivy.event import EventDispatcher
from kivy.clock import Clock

from multiprocessing import Process
from run_naga.widgets.kivy_component.file_browser import FileBrowser
from nagaclient import client as aclient

from os.path import expanduser
import os
import threading
import subprocess

from kivy.clock import Clock

Builder.load_file(os.path.dirname(__file__)+'/room_controller.kv')

class ClientGameProcess:
    def __init__(self, text,room_id,client_id,token,host='localhost'):
        super().__init__()
        #  self.cmd = ['python3','main.py','--load',text,
                                        #  '--room_id',room_id,
                                        #  '--host',host,
                                        #  '--client_id',client_id,
                                        #  '--token',token]
        process = subprocess.Popen('python3 '+expanduser("~")+'/projects/sim_map/main.py --load {0} --room_id {1} --host {2} --client_id {3} --token {4}'.format(text,room_id,host,client_id,token),shell=True)
class RoomController(Screen):
    def __init__(self,name=''):
        super().__init__(name=name)
        self.file_browser = FileBrowser(self)
        self.active_run = True
        self.entered =False
        self.ready = []
        self.num_player = 0

        self.menu_path = os.path.dirname(__file__)

        self.game_status = False

#        self.event = MyEventDispatcher().do_something('check')
#        self.game_client = aclient()

    def on_leave(self):
        self.entered=False

    def on_enter(self):
        print(self.manager.current_room_id)
        self.entered=True
        room_name =''
        response = self.manager.client_game.room.list_players()
        players = response['responses']['players']
        self.num_player = len(players)
        self.ids.room_name.text += self.manager.current_room_name
        self._trigger = Clock.schedule_interval(self.step,1)
        self.ids.current_player_number.text = 'Current Player in room:{0}'.format(self.num_player)

    def update(self,text):
        print(self.ids.file_client1.text)
        if text == 'client1':
            self.ids.file_client1.text = self.file_browser.file
        #  if text == 'client2':
            #  self.ids.file_client2.text = self.file_browser.file

    def step(self,*args):
        if self.entered and self.active_run:
            old_number = self.num_player
            response = self.manager.client_game.room.list_players()
            players = response['responses']['players']
            self.num_player = len(players)
            if self.num_player != old_number:
                self.ids.current_player_number.text = 'Current Player in room:{0}'.format(self.num_player)
            pass
            #self.manager

    def on_browse(self,text):
        if self.active_run:
            popup = self.file_browser
            popup.open()
            popup.client_browse=text
        #print(popup.file)

    def on_select_hero(self,text):
        if self.active_run:
            self.manager.client_game.room.select_hero(text)
            self.ids.select_hero.text = text

    def on_back(self):
        if self.active_run:
            self.manager.transition.direction = 'right'
            self.manager.current = 'lobby'

    def run_client1(self):
        print('1.{0}\n2.{1}\n3.{2}\n4.{3}'.format(self.manager.current_room_id,
                          self.manager.client_id,
                          self.manager.token,
                          self.manager.client_game._host))
#        self.manager.client_game.room.start_game()
        if self.active_run and self.ids.select_hero.text !='':
            self.active_run =False
#            self.manager.client_game.room.list_players()
            c = ClientGameProcess(self.ids.file_client1.text,
                              self.manager.current_room_id,
                              self.manager.client_id,
                              self.manager.token,
                              self.manager.client_game._host)
        App.get_running_app().stop()
        #  pass
