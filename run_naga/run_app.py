from kivy.app import App
from nagaclient.client import NagaClient
from .widgets.lobby import LobbyController
from .widgets.controller import NagaController
from .widgets.room_controller import RoomController
from kivy.uix.screenmanager import ScreenManager, Screen
from .widgets.login import LoginController
from .widgets.register_controller import RegisterController
import os
import json

class MyScreenManager(ScreenManager):
    def __init__(self,client_id=None,token_id='',host='localhost'):
        super().__init__()
        print(host)
        self.client_game = NagaClient(client_id=client_id,host=host,rpc_server=True)
        self.client_game.initial()
        self.current_room_id = ''
        self.current_room_name = ''
        self.status = ''
        self.user = ''
        self.client_id = ''
        self.token = token_id

    def exit(self):
        self.client_game.disconnect()

class RunApp(App):
    def build(self):
        with open(os.path.expanduser('~')+'/projects/sim_map/config.json') as data_file:
            data = json.load(data_file)
        print(data['page'])
        print(data['client_id'])
        print(data['token_id'])
        print(data['host'])
        client_id = data['client_id']

        if client_id !='' and data['token_id']!='' :
            print(data)
            self.msm = MyScreenManager(client_id=client_id, host=data['host'])
            self.msm.client_id = client_id
            self.msm.token = data['token_id']
            self.msm.client_game.user.loggedin_info = dict(token=data['token_id'],
                                          loggedin=True
                                            )
        else:
            self.msm = MyScreenManager(host=data['host'])

        self.msm.add_widget(LoginController(name='login'))
        self.msm.add_widget(RoomController(name='room'))
        self.msm.add_widget(LobbyController(name='lobby'))
        self.msm.add_widget(RegisterController(name='register'))
        self.msm.current = data['page']
        data['page']='login'
        data['client_id']=''
        data['token_id']=''
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)
        return self.msm
#        return NagaController()


    def on_stop(self):
        self.msm.exit()
        print('exit')
