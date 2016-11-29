from kivy.lang import Builder
from kivy.uix.popup import Popup
import os
from .warning_popup import WarningPopup
from os.path import expanduser

Builder.load_file(os.path.dirname(__file__) + '/file_browser.kv')

class FileBrowser(Popup):
    def __init__(self,controller):
        super().__init__(title="Browser")
        self.ids.browse_chooser.path = expanduser('~')
        self.file = None
        self.warning_popup = WarningPopup()
        self.controller = controller
        self.client_browse = ''

    def on_cancel(self):
        self.dismiss()

    def on_ok(self):
        if len(self.ids.browse_chooser.selection) != 0:
            self.file = self.ids.browse_chooser.selection[0]
            if self.ids.browse_chooser.selection[0][-3:] != '.py':
                self.warning_popup.open()
            else:
                self.file = self.ids.browse_chooser.selection[0]
                self.controller.update(self.client_browse)
                self.dismiss()
        else:
            self.warning_popup.open()

    def on_selection(self):
        if len(self.ids.browse_chooser.selection) != 0:
            self.ids.file_selected_input.text = self.ids.browse_chooser.selection[0]
            #print(self.ids.browse_chooser.selection[0])
