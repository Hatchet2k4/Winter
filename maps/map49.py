
import system

def to1():
    system.engine.mapSwitch('map46.ika-map', (22 * 16, 4.5 * 16))

def to47():
    y = system.engine.player.y
    system.engine.mapSwitch('map47.ika-map', (1 * 16, y))