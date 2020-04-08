import ika
import system
import savedata
import sound

from dragonpup import DragonGuard, DragonPup
from rune import GuardRune
from thing import Thing

def AutoExec():
    if 'guard48' not in savedata.__dict__:
        en = ika.Entity(162, 111, system.engine.player.layer, 'dragonpup.ika-sprite')
        en.name = 'dragonp'
        e = DragonPup(en)
        system.engine.addEntity(e)            
        system.engine.things.append(DeathListener(e)) 

        en = ika.Entity(162, 111, system.engine.player.layer, 'guardrune.ika-sprite')
        en.name = 'guard48'
        system.engine.addEntity(GuardRune(en))
        
        # listen for dragonpup to be dead to drop a guard rune
                

def to47():
    offset_from = 18 * 16  # first horizontal pos possible
    offset_to = 81 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map47.ika-map', (x, 1 * 16))
    
class DeathListener(Thing): #for SoulReaver quest
    def __init__(self, e=None):
        self.ent = e
        
        
    def update(self):    
          
        pass 
        """
        e= system.engine.entFromEnt[
                ika.Map.entities['dragonp']
                ]       
        ika.Log(str(e)) #None?!
    
        if e.stats.hp == 0:            
            en = ika.Entity(162, 111, system.engine.player.layer, 'guardrune.ika-sprite')
            en.name = 'guard48'
            system.engine.addEntity(GuardRune(en))
            return True
        """

    def draw(self):
        pass


