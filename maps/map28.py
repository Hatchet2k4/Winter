import ika
import system
    
def to27():
    offset_from = 13 * 16  # first vertical pos possible
    offset_to = 33 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map27.ika-map', (x, 1 * 16))