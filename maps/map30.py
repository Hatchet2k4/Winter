
import system
import savedata

from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))    
    
    
def to25():
    system.engine.mapSwitch('map25.ika-map', (39 * 16, 5 * 16))

def to31():
    x = system.engine.player.x + 16
    system.engine.mapSwitch('map31.ika-map', (x, 28 * 16))
    

