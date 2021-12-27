
import system
import savedata

from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))    
    
    
def to25():
    system.engine.mapSwitch('map25.ika-map', (22 * 16, 3 * 16+1))

def to31():
    x = system.engine.player.x
    system.engine.mapSwitch('map31.ika-map', (x, 28 * 16))
    

