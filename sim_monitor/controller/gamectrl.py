from cocos.layer import Layer
from cocos.scene import Scene
from sim_monitor.model.status import status

class GameCtrl( Layer ):
    def __init__(self, model) :
        super().__init__()
        self.model = model
        self.timer = 0

    def resume_controller( self ):
        self.schedule(self.step)

    def step(self, dt):
        self.timer +=dt
        if self.timer > 1:
            self.timer = 0
            print(dt)
#            if status
            self.model.check_connecting()
