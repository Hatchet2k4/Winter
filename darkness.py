import ika
from thing import Thing
import system

class Darkglow(Thing):
    circleimage = ika.Image('gfx/circle_gradient.png')
    
    def draw(self):
        p=system.engine.player
        x=int(p.x + 8 - ika.Map.xwin) - 640
        y=int(p.y - ika.Map.ywin) - 480
        ika.Video.TintBlit(self.circleimage, x,y, ika.RGB(180,210,250,200), ika.SubtractBlend)