from kivy.app import App
from nagaclient.client import NagaClient
from .widgets.lobby import LobbyController
from .widgets.controller import NagaController
from .widgets.room_controller import RoomController
from kivy.uix.screenmanager import ScreenManager, Screen
from .widgets.login import LoginController

sm = ScreenManager()
sm.add_widget(LoginController(name='login'))
sm.add_widget(RoomController(name='room'))
sm.add_widget(LobbyController(name='lobby'))

class MyScreenManager(ScreenManager):
    def __init__(self):
        super().__init__()
        self.client_game = NagaClient(rpc_server=True)
        self.client_game.initial()
        self.current_room_id = ''
        self.current_room_name = ''
        self.status = ''
        self.user = ''
        self.client_id =''
        self.token =''

class RunApp(App):
    def build(self):
        msm = MyScreenManager()
        msm.add_widget(LoginController(name='login'))
        msm.add_widget(RoomController(name='room'))
        msm.add_widget(LobbyController(name='lobby'))
        return msm
