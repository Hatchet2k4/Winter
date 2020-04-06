
import system
from dragonpup import DragonGuard
from rune import Gua

def AutoExec():
    if 'guard48' not in savedata.__dict__:
        e = [
            DragonGuard(ika.Entity(162, 111, system.engine.player.layer, 'dragonpup.ika-sprite'))
            ]
        system.engine.things.append(DeathListener(e)) # listen for dragonpup to be dead to drop a guard rune
                

def to47():
    offset_from = 18 * 16  # first horizontal pos possible
    offset_to = 81 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map47.ika-map', (x, 1 * 16))
    
    
class DeathListener(Thing): 

    def __init__(self, e=None):
        self.enemies = e

    def update(self):
        done = True
        for e in self.enemies:
            if e.stats.hp > 0:
                done = False
        if done: #all are dead                        
            e = ika.Entity(162, 111, system.engine.player.layer, 'guardrune.ika-sprite')
            e.name = 'guard48'
            system.engine.addEntity(GuardRune(e))
            
            return True

    def draw(self):
        pass