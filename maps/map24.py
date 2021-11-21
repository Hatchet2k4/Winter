
import system
import ika
import savedata

from thing import Thing
from rune import CowardRune
import sound
from soulreaver import SoulReaver
from obstacle import Crystal
import cabin


def AutoExec():    
    pass


def forebattle():
    #if 'unityrune' in savedata.__dict__ and 'forebattle' not in savedata.__dict__: 
    #    system.engine.clearKillQueueCabin()
    #    cabin.scene('forebattle')      
    #    system.engine.camera.center()
    pass
    
def manaPool():
    if 'unityrune' in savedata.__dict__ or 'penultimatebattle' not in savedata.__dict__:
        system.engine.player.stats.mp += 1        
        
def to23():
    if 'unityrune' in savedata.__dict__ and 'forebattle' not in savedata.__dict__: 
        system.engine.clearKillQueueCabin()
        cabin.scene('forebattle')      
        system.engine.camera.center()
    system.engine.mapSwitch('map23.ika-map', (5 * 16, 5 * 16))
    
def to50():
    system.engine.mapSwitch('map50.ika-map', (9 * 16, 13 * 16))
    
def kaboom():
    #nearend quest completed!
    if 'penultimatebattle' not in savedata.__dict__ and 'waterguard' in savedata.__dict__ and 'windguard' in savedata.__dict__ and 'fireguard' in savedata.__dict__:        
        savedata.penultimatebattle = 'True'
        p = system.engine.player
        
        def noOp():
            while True:
                yield None
        
        p.anim = 'stand'
        p.state = noOp()
        sound.playMusic('music/resurrection.it')        
        for n in range(150):
            # teh earthquake
            ika.Map.xwin += ika.Random(-3, 3)
            ika.Map.ywin += ika.Random(-3, 3)
            system.engine.tick()
            system.engine.draw()
            ika.Video.ShowPage()
            ika.Input.Update()
        
        e = ika.Entity(48*16-8, 9*16, 2, 'crystal.ika-sprite')
        e.name = 'penultimatecrystal'
        system.engine.addEntity(Crystal(e))      

        y = SoulReaver(ika.Entity(20*16, 20*16, 2, 'soulreaver.ika-sprite'))
        system.engine.addEntity(y)
        system.engine.mapThings.append(DeathListener(y))
        
        p.state = p.defaultState()
        system.engine.synchTime()

class DeathListener(Thing):
    'Waits until the soulreaver is dead, then drops the final rune.'
    def __init__(self, yeti=None):
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            e = ika.Entity(315, 320, 2, 'unityrune.ika-sprite')
            e.name = 'unityrune'
            system.engine.addEntity(UnityRune(e))    
            sound.playMusic("music/lampoons.it")
            savedata.finalrune = 'True'
            return True

    def draw(self):
        pass
    

        