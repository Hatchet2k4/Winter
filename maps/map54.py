import ika
import system

def to01():
    #offset_from = 8 * 16  # first vertical pos possible
    #offset_to = 22 * 16  # first vertical pos possible
    #y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map01.ika-map', (53 * 16, 6*16))