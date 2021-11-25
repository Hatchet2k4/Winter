import system
from snow import Snow
import cabin
import savedata

def AutoExec():
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))    

def nearEnd():    
    pass
    



def to30():
    x = system.engine.player.x - 160
    system.engine.mapSwitch('map30.ika-map', (6 * 16 + x, 16))
    if 'nearend' not in savedata.__dict__:
        cabin.scene('nearend') #automatically adds scene to savedata    

def to32():
    # no adjustment here on purpose
    system.engine.mapSwitch('map32.ika-map', (25 * 16, 38 * 16))