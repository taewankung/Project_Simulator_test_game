from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from multiprocessing import Process

from os.path import expanduser
import os
import threading
import subprocess

Builder.load_file(os.path.dirname(__file__)+'/register_controller.kv')

class RegisterController(Screen):
    def __init__(self,name='register'):
        super().__init__(name=name)

#    def on_login(self):
    def on_register_user(self,user,password,email,first_name,last_name):
        try:
            response = self.manager.client_game.user.register(user,password,email,first_name,last_name)
            args = response['args']
            self.manager.current = 'login'
        except Exception as ex:
            print(ex)
            print('plz open server')
            self.ids.report.color = [1,0,0,1]
            self.ids.report.text ='Can not connect to server'
            self.ids.report.font_size =30
            self.ids.bold = True

    def on_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'
        #self.manager.transition.direction = 'left'
#        logined = response['responses']['loggedin']
#        if logined:
#            self.manager.client_id = response['client_id']
#            self.manager.user = args['username']
#            self.manager.token = response['responses']['token']
#            self.manager.current = 'lobby'
