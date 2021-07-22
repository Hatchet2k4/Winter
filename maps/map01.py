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

def to2():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 38 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map02.ika-map', (48 * 16, y))

def to49():
    system.engine.mapSwitch('map54.ika-map', (3 * 16, 12 * 16))

class RuneListener(object):
    def update(self):
        if 'waterguard' in savedata.__dict__ and 'fireguard' in savedata.__dict__ and 'windguard' in savedata.__dict__:
            system.engine.addEntity(
                Yeti(ika.Entity(35 * 16, 19 * 16, system.engine.player.layer, 'yeti.ika-sprite')))        
            return True

    def draw(self):
        pass