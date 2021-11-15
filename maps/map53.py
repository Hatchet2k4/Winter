import ika
import system

from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(600, velocity=(.4, 1), colour=ika.RGB(192,192,255)))
    system.engine.background = ika.Image('gfx/mountains.png')

def to39():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 34 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map39.ika-map', (38 * 16, y))
    
def to41():
    offset_from = 8 * 16  # first vertical pos possible
    offset_to = 8 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map41.ika-map', (1 * 16, y))