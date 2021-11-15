import ika
import system
import savedata
import sound
from thing import Thing


from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(6000, velocity=(-1.2, 3)))
    sound.playMusic("music/wind.ogg")
                
def to47():
    system.engine.mapSwitch('map47.ika-map', (38*16, 4 * 16))

def manaPool():    
    system.engine.player.stats.mp += 1


