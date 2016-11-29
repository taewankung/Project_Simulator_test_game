from kivy.app import App
from .widgets.controller import NagaController
class RunApp(App):
    def build(self):
        return NagaController()
