import ika
import system
import savedata
import cabin

from yeti import Yeti
from snow import Snow


def AutoExec():
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))
    if 'unityrune' not in savedata.__dict__:
        system.engine.things.append(RuneListener())
    #if 'introanim' not in savedata.__dict__:
    system.engine.things.append(IntroAnim())
    #    savedata.introanim = True
                
            
        
        
        

def to2():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 38 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map02.ika-map', (48 * 16, y))

def to49():
    system.engine.mapSwitch('map54.ika-map', (3 * 16, 12 * 16))

class IntroAnim(object):    
    def __init__(self):
        self.d = 0
        
    def update(self):        
        p = system.engine.player;
        p.stop()
        p._state = lambda: None # keep the player from moving
        p.ent.specframe=74
        
        for i in range(200):
            ika.Input.Update()
            ika.ProcessEntities()
            system.engine.camera.update()
            system.engine.draw()
            ika.Video.ShowPage()
            ika.Delay(1)
            
        p.ent.specframe=72            
        for i in range(100):
            ika.Input.Update()
            ika.ProcessEntities()
            system.engine.camera.update()
            system.engine.draw()
            ika.Video.ShowPage()
            ika.Delay(1)        
        
        p.state = p.standState()
        system.engine.synchTime()
        return True        

    def draw(self):
        pass

class RuneListener(object):
    def update(self):
        if 'waterguard' in savedata.__dict__ and 'fireguard' in savedata.__dict__ and 'windguard' in savedata.__dict__:
            system.engine.addEntity(
                Yeti(ika.Entity(35 * 16, 19 * 16, system.engine.player.layer, 'yeti.ika-sprite')))        
            return True

    def draw(self):
        pass