import shutil,errno
import os
import inspect
import importlib
from .api_game.my_hero import MyHero
import datetime
import time
import hashlib
from sim_monitor.model.status import status
#from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient
import threading

def copy_file(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

class Executor(threading.Thread):
    def __init__(self):
        super().__init__()
        self.ex_lib = None
        self.hero = MyHero()
        self.ready_time = datetime.datetime.now()
        #self.ac = ApaimaneeMOBAClient()

    def load_file(self,module=""):
        string = ''
        #for text in module.split('.'):
        #    string = string+'/'+text
        print(module)
        copy_file(module,str(os.path.dirname(__file__)+'/ex_code'))
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()

        with open(module,'rb') as opened_file:
            #  testing_read = opened_file.read()
            #  print(testing_read)
#            testing = sha1.update(str(testing_read))
#            print('sha1_test: '+sha1.hexdigest())
            print("empty SHA1: {0}".format(sha1.hexdigest()))
            readFile =0
            while readFile !=b'':
                readFile = opened_file.read(BUF_SIZE)
                sha1.update(readFile)
                print("SHA1: {0}".format(sha1.hexdigest()))
            opened_file.close()

        print("MD5: {0}".format(md5.hexdigest()))
        print("SHA1: {0}".format(sha1.hexdigest()))
        status.hash_file = sha1.hexdigest()
        my_file = module.split('/')[-1]
        print(my_file.split('.')[0])
        module="sim_monitor.sim_client.ex_code."+my_file.split('.')[0]

        #  sha1Hash = hashlib.sha1(readFile)
        #  sha1Hashed = sha1Hash.hexdiigest()
        #  print(''+sha1Hashed)

        #  status.hash_file = sha1Hashed
        try:
            self.ex_lib = importlib.import_module(module)
            print("load_module complete")
            for name,obj in inspect.getmembers(self.ex_lib):
                if inspect.isclass(obj) and issubclass(obj,MyHero) and obj is not MyHero:
                    print(obj)
                    self.hero = obj()

        except ValueError:
            print("cannot import module: "+module)
            #return self.ex_lib
        return self.ex_lib

    def run(self):
        if status.connect:
            try:
                self.hero.run()
            except Exception as e :
                print("Exeception in Executor"+str(e))

#  if __name__ == "__main__":
      #  ex = Executor("api_game.apaimanee","api_game")
      #  ex.run()
