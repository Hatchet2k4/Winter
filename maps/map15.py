import system
import ika
from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(3000, velocity=(-1, 1.5)))

def to2():
    offset_from = 16 * 16  # first vertical pos possible
    offset_to = 7 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map02.ika-map', (x, 1 * 16))
    
def to18():    
    system.engine.mapSwitch('map18.ika-map', (11*16, 73*16))