
import system

from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(5000, velocity=(-.5, 2)))
    
def to2():
    offset_from = 6 * 16  # first horizontal pos possible
    offset_to = 14 * 16  # first horizontal pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map02.ika-map', (1 * 16, y))

def to4():
    offset_from = 8 * 16  # first horizontal pos possible
    offset_to = 11 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map04.ika-map', (x, 38 * 16))
