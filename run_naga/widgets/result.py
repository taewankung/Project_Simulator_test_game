from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from multiprocessing import Process
from run_naga.widgets.kivy_component.file_browser import FileBrowser
#from naga

from os.path import expanduser
import os
import json
import re

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp

Builder.load_file(os.path.dirname(__file__)+'/result.kv')

class ResultLabel(TextInput):
    def __init__(self,manager=None,text='',size_hint_y=None, height=200):
        super().__init__(text=text,size_hint_y=size_hint_y, height=height)
        self.manager = manager

class ResultController(Screen):
    def __init__(self,name=''):
        super().__init__(name=name)
        self.result_box = self.ids.result_box
        #  self.result_box.bind(minimum_height = self.result_box.setter('height'))

    def on_next(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'lobby'

    def on_enter(self):
        with open(os.path.dirname(__file__)+'/../../config.json') as data_file:
            data = json.load(data_file)
        my_path = data['old_file']
#        mystr = data.read(10);
        #  print(my_path)
        result_file = open(my_path)
        result_text = str(result_file.read())
        #  result_label = ResultLabel(text=result_text)
        #self.result_box.
        self.result_box.text = result_text
        result_file.close()
        pass
