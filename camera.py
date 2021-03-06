import ika
import system
from thing import Thing

class Camera(Thing):
    def __init__(self):
        super(Camera, self).__init__()
        self.locked = False

    def update(self):
        if not self.locked:
            x = system.engine.player.x - ika.Video.xres / 2
            y = system.engine.player.y - ika.Video.yres / 2
            ika.Map.ywin += y > ika.Map.ywin
            ika.Map.ywin -= y < ika.Map.ywin
            ika.Map.xwin += x > ika.Map.xwin
            ika.Map.xwin -= x < ika.Map.xwin

    def center(self):
        ika.Map.xwin = system.engine.player.x - ika.Video.xres / 2
        ika.Map.ywin = system.engine.player.y - ika.Video.yres / 2
