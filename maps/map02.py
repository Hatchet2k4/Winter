
import system

from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(3000, velocity=(-1, 1.5)))

def to1():
    offset_from = 38 * 16  # first vertical pos possible
    offset_to = 4 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map01.ika-map', (1 * 16, y))

def to3():
    offset_from = 14 * 16  # first vertical pos possible
    offset_to = 6 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map03.ika-map', (98 * 16, y))

def to15():
    offset_from = 7 * 16  # first vertical pos possible
    offset_to = 7 * 16  # first vertical pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map15.ika-map', (x, 43 * 16))

def to43():
    system.engine.mapSwitch('map43.ika-map', (1 * 16, system.engine.player.y))