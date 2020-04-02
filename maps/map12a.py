import system
import saveloadmenu
import dir

def to12():
    system.engine.mapSwitch('map11.ika-map', (23 * 16, 17 * 16))

def to5():
    system.engine.mapSwitch('map11.ika-map', (23 * 16, 17 * 16))

def to27():
    system.engine.mapSwitch('map11.ika-map', (23 * 16, 17 * 16))

def heal():
    system.engine.player.stats.hp = 999
    system.engine.player.stats.mp = 999
