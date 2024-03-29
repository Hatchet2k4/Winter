
import system

def to55():
    system.engine.mapSwitch('map55.ika-map', (14 * 16, 38 * 16))
    
def to48():
    offset_from = 81 * 16  # first horizontal pos possible
    offset_to = 18 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map48.ika-map', (x, 28 * 16))
    
def to49():
    y = system.engine.player.y
    system.engine.mapSwitch('map49.ika-map', (43 * 16, y))