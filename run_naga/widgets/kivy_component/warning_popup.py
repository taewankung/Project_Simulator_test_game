from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

Builder.load_file(os.path.dirname(__file__)+'/warning_popup.kv')

class WarningPopup(Popup):
    def __init__(self):
        super().__init__(title='Warning')

    def on_ok(self):
        self.dismiss()
