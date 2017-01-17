from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from multiprocessing import Process
from run_naga.widgets.kivy_component.file_browser import FileBrowser
from nagaclient import client as aclient

from os.path import expanduser
import os
import threading
import subprocess

Builder.load_file(os.path.dirname(__file__)+'/room_controller.kv')

class ClientGameProcess(Process):
    def __init__(self, text,room_id,client_id,token,host='localhost'):
        super().__init__()
        self.cmd = ['python3','main.py','--load',text,
                                        '--room_id',room_id,
                                        '--host',host,
                                        '--client_id',client_id,
                                        '--token',token]

    def run(self):
        process = subprocess.call(self.cmd)

class RoomController(Screen):
    def __init__(self,name=''):
        super().__init__(name=name)
        self.file_browser = FileBrowser(self)
#        self.game_client = aclient()

    def on_enter(self):
        print(self.manager.current_room_id)
        room_name =''
        self.ids.room_name.text += self.manager.current_room_name

    def update(self,text):
        print(self.ids.file_client1.text)
        if text == 'client1':
            self.ids.file_client1.text = self.file_browser.file
        #  if text == 'client2':
            #  self.ids.file_client2.text = self.file_browser.file

    def on_browse(self,text):
        popup = self.file_browser
        popup.open()
        popup.client_browse=text
        #print(popup.file)

    def run_client1(self):
        print('1.{0}\n2.{1}\n3.{2}\n4.{3}'.format(self.manager.current_room_id,
                          self.manager.client_id,
                          self.manager.token,
                          self.ids.host.text))
        self.manager.client_game.room.list_players()
#        self.manager.client_game.room.start_game()
        ClientGameProcess(self.ids.file_client1.text,
                          self.manager.current_room_id,
                          self.manager.client_id,
                          self.manager.token,
                          self.ids.host.text).start()
        #  pass
