import cocos

class Bar(cocos.layer.ColorLayer):
    def __init__(self,r=0,b=255,g=0,a=100,width=100,height=10):
        super().__init__(r,b,g,a,width=width,height=height)
        self.transform_anchor_x=0
    def update(self,current_hp,max_hp):
        self.current_hp = current_hp
        self.scale_x = self.current_hp/max_hp

