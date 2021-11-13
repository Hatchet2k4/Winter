import system
import saveloadmenu
import dir

def to12():
    offset_from = 7 * 16  # first vertical pos possible
    offset_to = 6 * 16  # first vertical pos possible
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map12.ika-map', (1 * 16, y))

def to52():
    system.engine.mapSwitch('map52.ika-map', (29 * 16, 5 * 16))




