import ika
import system
import savedata
import sound
from thing import Thing
from yeti import Yeti
from soulreaver import SoulReaver
from razormane import RazorMane

from snow import Snow

def AutoExec():
    system.engine.mapThings.append(Snow(6000, velocity=(-.2, 3)))
    sound.playMusic("music/wind.ogg")
                
def to47():
    offset_from = 11 * 16  # first horizontal pos possible
    offset_to = 8 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map47.ika-map', (x, 1 * 16))

def manaPool():    
    system.engine.player.stats.mp += 1


