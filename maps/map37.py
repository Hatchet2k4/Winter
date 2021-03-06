import ika
import system
import savedata

from carnivore import Carnivore
from snow import Snow

spawned = 0

def AutoExec():
    global spawned
    spawned = 0
    system.engine.mapThings.append(Snow(100, velocity=(.4, 1), colour=ika.RGB(255,192,255)))
    system.engine.background = ika.Image('gfx/mountains.png')
    
def to36():
    system.engine.mapSwitch('map36.ika-map', (system.engine.player.x, 1 * 16))
    
def releaseAnklebiters():

    global spawned
    
    if not 'dynamite3' in savedata.__dict__.keys() and not spawned:
        
        indeces = ((6,6), (9,6), (12,6), (4, 8), (14, 8), (2, 10), (6, 10), (12, 10), (16, 10),
                   (4,11), (14, 11))
                   
        for i in indeces:
            system.engine.addEntity(Carnivore(ika.Entity(i[0]*16+8, i[1]*16, 1, "carnivore.ika-sprite")))
            
        spawned = 1