import system
import ika
from snow import Snow
from thing import Thing


def to18():
    system.engine.mapSwitch('map18.ika-map', (32*16, 4*16))
    
def to6():
    offset_from = 5 * 16  # first vertical pos possible
    offset_to = 16 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map06.ika-map', (x, 38 * 16))
    
    
