import system
import saveloadmenu
import dir

def to11():
    system.engine.mapSwitch('map11.ika-map', (23 * 16, 17 * 16))

def to12a():
    offset_from = 6 * 16  # first vertical pos possible on current
    offset_to = 7 * 16  # first vertical pos possible on destination
    y = system.engine.player.y - offset_from + offset_to
    system.engine.mapSwitch('map12a.ika-map', (18 * 16, y))


def heal():
    system.engine.player.stats.hp = 999
    system.engine.player.stats.mp = 999
