
import system
import ika
from snow import Snow

def AutoExec():
    system.engine.background = ika.Image('gfx/mountains.png')
    system.engine.mapThings.append(Snow(velocity=(0, 0.5)))

def to20():
    offset_from = 19 * 16  # first vertical pos possible
    offset_to = 5 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map20.ika-map', (x, 1 * 16))

def to7():
    offset_from = 4 * 16  # first vertical pos possible
    offset_to = 21 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map07.ika-map', (1 * 16, y))

def to8():
    offset_from = 3 * 16  # first vertical pos possible
    offset_to = 29 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map08.ika-map', (48 * 16, y))
