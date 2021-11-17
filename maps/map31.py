import system
from snow import Snow
import cabin

def AutoExec():
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))    

def nearEnd():
    #system.engine.things.append(CabinListener())
    if 'nearend' not in savedata.__dict__:
        cabin.scene('nearend') #automatically adds scene to savedata    

class CabinListener(object):
    def update(self):
        if 'nearend' not in savedata.__dict__:
            cabin.scene('nearend') #automatically adds scene to savedata
            return True

    def draw(self):
        pass


def to30():
    x = system.engine.player.x - 160
    system.engine.mapSwitch('map30.ika-map', (6 * 16 + x, 16))
    

def to32():
    # no adjustment here on purpose
    system.engine.mapSwitch('map32.ika-map', (25 * 16, 38 * 16))