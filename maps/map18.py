import system
import ika
from snow import Snow
from thing import Thing
from darkness import Darkglow

fader = Thing()

def AutoExec():
    global fader
    fader = LayerFader()
    system.engine.mapThings.append(fader)
    system.engine.mapThings.append(Darkglow())

def to20():
    system.engine.mapSwitch('map20.ika-map', (22*16, 12*16))
    
def to15():
    system.engine.mapSwitch('map15.ika-map', (10*16, 6*16+8))
    
    
class LayerFader(Thing):
    def __init__(self):
        self.fade = 255
        self.layer = ika.Map.FindLayerByName('Hidden') 
        self.startfade = False
        self.x=5*16
        self.w=7*16
        self.y=44*16
        self.h=8*16
        self.color = ika.RGB(0,0,0,255)
        
    def update(self):    
        if(self.startfade and self.fade>0):         
            self.fade=max(self.fade-3, 0)
            self.color=ika.RGB(0,0,0,self.fade)
            
    def draw(self):
        x=self.x - ika.Map.xwin
        y=self.y - ika.Map.ywin
        ika.Video.DrawRect(x, y,x+self.w,y+self.h,self.color, True)
    
def layerfader():
    global fader
    fader.startfade=True
    