import ika
from thing import Thing
import system

class Darkglow(Thing):
    circleimage = ika.Image('gfx/circle_gradient.png')
    
    def draw(self):
        p=system.engine.player
        x=int(p.x + 8 - ika.Map.xwin) - 320
        y=int(p.y - ika.Map.ywin) - 240
        ika.Video.TintBlit(self.circleimage, x,y, ika.RGB(255,255,255,192), ika.SubtractBlend)