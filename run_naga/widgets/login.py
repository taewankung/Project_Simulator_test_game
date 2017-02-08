from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from multiprocessing import Process
#from run_naga.widgets.kivy_component.file_browser import FileBrowser

from os.path import expanduser
import os
import threading
import subprocess

Builder.load_file(os.path.dirname(__file__)+'/login.kv')

class LoginController(Screen):
    def __init__(self,name='login'):
        super().__init__(name=name)

    def on_login(self,user,password):
        try:
            response = self.manager.client_game.user.login(user,password)
            args = response['args']
            logined = response['responses']['loggedin']
            if logined:
                self.manager.client_id = response['client_id']
                self.manager.user = args['username']
                self.manager.token = response['responses']['token']
                self.manager.transition.direction = 'left'
                self.manager.current = 'lobby'
        except Exception as test:
            print(test)
            print('plz open server')
            self.ids.report.color = [1,0,0,1]
            self.ids.report.text ='Can not connect to server'
            self.ids.report.font_size =30
            self.ids.bold = True

    def on_register_user(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'register'
