from kivy.app import App
from nagaclient.client import NagaClient
from .widgets.lobby import LobbyController
from .widgets.controller import NagaController
from .widgets.room_controller import RoomController
from kivy.uix.screenmanager import ScreenManager, Screen
from .widgets.login import LoginController
from .widgets.register_controller import RegisterController

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

    def exit(self):
        self.client_game.disconnect()

class RunApp(App):
    def build(self):
        self.msm = MyScreenManager()
        self.msm.add_widget(LoginController(name='login'))
        self.msm.add_widget(RoomController(name='room'))
        self.msm.add_widget(LobbyController(name='lobby'))
        self.msm.add_widget(RegisterController(name='register'))
        return self.msm
#        return NagaController()

    def on_stop(self):
        self.msm.exit()
        print('exit')
