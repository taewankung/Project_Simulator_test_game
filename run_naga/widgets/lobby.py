from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from multiprocessing import Process
from run_naga.widgets.kivy_component.file_browser import FileBrowser
#from naga

from os.path import expanduser
import os

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp

Builder.load_file(os.path.dirname(__file__)+'/lobby.kv')

class RoomButton(Button):
    def __init__(self,room_id,manager=None,text='',size_hint_y=None, height=40):
        super().__init__(text=text,size_hint_y=size_hint_y, height=height)
        self.manager = manager
        self.room_id = room_id

    def on_press(self):
        self.manager.current_room_id = self.room_id
        self.manager.client_game.room.join_game(self.manager.current_room_id)
        self.manager.current_room_name =self.text
        self.manager.transition.direction = 'left'
        self.manager.current='room'



class LobbyController(Screen):
    def __init__(self,name=''):
        super().__init__(name=name)
        self.room_layout = self.ids.room_list
        self.room_layout.bind(minimum_height = self.room_layout.setter('height'))

    def on_refresh(self):
        try:
            response = self.manager.client_game.room.list_rooms()
            args = response['args']
            rooms = response['responses']['rooms']
            self.room_layout.clear_widgets()
            for room in rooms:
                room_name = room[1]['room_name']
                self.room_layout.add_widget(RoomButton(room[0],self.manager,text=room_name))
        except Exception as ex:
            print(ex)
            print('plz open server')
            self.ids.report.color = [1,0,0,1]
            self.ids.report.text ='Can not connect to server'
            self.ids.report.font_size =30
            self.ids.bold = True

    def on_create(self):
        try:
            room_name= self.ids.room_name.text
            responses = self.manager.client_game.room.create_room(room_name)
            response = responses['responses']
            args = responses['args']
            self.manager.current_room_id = response['room_id']
            self.manager.current_room_name = room_name
            self.manager.client_game.room.join_game(self.manager.current_room_id)
            self.manager.transition.direction = 'left'
#        print(self.manager.client_id)
            self.manager.current='room'
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

    def on_enter(self):
        self.on_refresh()


        #  for i in range(100):
            #  btn = Button(text=str(i), size_hint_y=None, height=40)
            #  layout.add_widget(btn)
#        root = self.ids.scollview
#        runTouchApp(root)
       #  layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
##   Make sure the height is such that there is something to scroll.
        #  layout.bind(minimum_height=layout.setter('height'))
        #  for i in range(100):
            #  btn = Button(text=str(i), size_hint_y=None, height=40)
            #  layout.add_widget(btn)
        #  root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        #  root.add_widget(layout)

        #  runTouchApp(root)

#        self.naga_client = naga_client


