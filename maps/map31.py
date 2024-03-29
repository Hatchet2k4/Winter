import system
from snow import Snow
import cabin
import savedata

def AutoExec():
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))    

def nearEnd():    
    if 'nearend' not in savedata.__dict__:
        system.engine.clearKillQueueCabin()
        cabin.scene('nearend') #automatically adds scene to savedata    
        system.engine.camera.center()
    



def to30():
    x = system.engine.player.x
    system.engine.mapSwitch('map30.ika-map', (x, 16))
    

def to32():
    # no adjustment here on purpose
    system.engine.mapSwitch('map32.ika-map', (25 * 16, 38 * 16))