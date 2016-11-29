from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from multiprocessing import Process
from run_naga.widgets.kivy_component.file_browser import FileBrowser

from os.path import expanduser
import os
import threading
import subprocess

Builder.load_file(os.path.dirname(__file__)+'/controller.kv')

class Client1(Process):
    def __init__(self, text='run_naga/api_code/test.py',host='localhost'):
        super().__init__()
        self.cmd = ['python3','main.py','--load',text,'--host',host]

    def run(self):
        process = subprocess.call(self.cmd)

class Client2(Process):
    def __init__(self, text='run_naga/api_code/test.py',host='localhost'):
        super().__init__()
        self.cmd = ['python3','main.py', '--client', 'client1' ,'--token' ,'client1','--load',text,'--host',host]

    def run(self):
        process = subprocess.call(self.cmd)

class CommandRunner(threading.Thread):
    def __init__(self,command):
        super().__init__()
        self.command = command
        self.output = []

    def run(self):
        output = subprocess.check_output(self.command)
        self.output.remove('')

class NagaController(FloatLayout):
    def __init__(self):
        super().__init__()
        self.file_browser = FileBrowser(self)
        pass

    def active_env(self):
        #output = supprocess.check_output('source','../naga-env/bin/activate')
        #print(output)
        pass

    def update(self,text):
        #print(self.ids.file_client1.text)
        if text == 'client1':
            self.ids.file_client1.text = self.file_browser.file
        if text == 'client2':
            self.ids.file_client2.text = self.file_browser.file

    def on_browse(self,text):
        popup = self.file_browser
        popup.open()
        popup.client_browse=text
        print(popup.file)

    def run_client1(self):
        Client1(self.ids.file_client1.text,self.ids.host.text).start()
        pass

    def run_client2(self):
        Client2(self.ids.file_client2.text,self.ids.host.text).start()
        pass
