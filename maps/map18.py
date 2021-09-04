import system
import ika
from snow import Snow
from thing import Thing

fader = Thing()

def AutoExec():
    global fader
    fader = LayerFader()
    system.engine.mapThings.append(fader)

def to2():
    offset_from = 16 * 16  # first vertical pos possible
    offset_to = 7 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map02.ika-map', (x, 1 * 16))
    
def to18():    
    system.engine.mapSwitch('map18.ika-map', (0, 0))

def to12():
    pass
    
def to15():
    pass
    
    
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
    