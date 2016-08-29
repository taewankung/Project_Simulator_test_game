
import cocos
import pyglet
import weakref
import time
from .status import status
from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
class GameModel( pyglet.event.EventDispatcher ):
    def __init__(self):
        super().__init__()
        self.ac = None

    def set_controller(self,ctrl):
        self.ctrl = weakref.ref(ctrl)
        pass
    def start(self):
        self.connection()

    def connection(self):
        self.ctrl().resume_controller()
        self.dispatch_event("on_connection")

    def check_connecting(self):
        if not status.connect:
            print("connecting...")
        else:
            self.ac =ApaimaneeMOBAClient()
            time.sleep(2)
        self.dispatch_event("check_connecting")

GameModel.register_event_type('check_connecting')
GameModel.register_event_type('on_connection')
