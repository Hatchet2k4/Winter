import system
import saveloadmenu
import dir

def to12():
    offset_from = 7 * 16  # first vertical pos possible
    offset_to = 6 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map12.ika-map', (1 * 16, y))

def to5():
    system.engine.mapSwitch('map05.ika-map', (6 * 16, 4 * 16))

#def to27():
#    system.engine.mapSwitch('map11.ika-map', (23 * 16, 17 * 16))

def heal():
    system.engine.player.stats.hp = 999
    system.engine.player.stats.mp = 999
