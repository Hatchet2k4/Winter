import system
import ika

#from darkness import Darkglow

#def AutoExec():
#    system.engine.mapThings.append(Darkglow())

def to23():
    system.engine.mapSwitch('map23.ika-map', (6 * 16, 42 * 16))

def to26():
    offset_from = 50 * 16  # first vertical pos possible
    offset_to = 20 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map26.ika-map', (38 * 16, y))

def to30():
    system.engine.mapSwitch('map30.ika-map', (9*16, 21*16))