import ika
import system
from thing import Thing

class Camera(Thing):
    def __init__(self):
        super(Camera, self).__init__()
        self.locked = False
        self.speed=1
        self.time=0
        
    def speedup(self, t=50):
        self.speed=2
        self.time=t

    def update(self):
        if self.time>0: self.time-=1
    
        if not self.locked:
            x = system.engine.player.x - ika.Video.xres / 2
            y = system.engine.player.y - ika.Video.yres / 2
            ika.Map.ywin += int(y > ika.Map.ywin) * self.speed
            ika.Map.ywin -= int(y < ika.Map.ywin) * self.speed
            ika.Map.xwin += int(x > ika.Map.xwin) * self.speed
            ika.Map.xwin -= int(x < ika.Map.xwin) * self.speed
            if abs(ika.Map.xwin - x) < 4 and abs(ika.Map.ywin - y) < 4 and self.time==0:
                self.speed=1
            
    def center(self):
        ika.Map.xwin = system.engine.player.x - ika.Video.xres / 2
        ika.Map.ywin = system.engine.player.y - ika.Video.yres / 2
