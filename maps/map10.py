import system
import ika
from yeti import Yeti
from soulreaver import SoulReaver
from thing import Thing
from rune import FireRune
from obstacle import IceWall
import savedata
import sound
import cabin
from caption import Caption

def AutoExec():                 
    if 'fireguard' not in savedata.__dict__ and 'nearend' in savedata.__dict__: #final quest active            
        system.engine.mapThings.append(SetupBattle())        
    if 'bossin10' in savedata.__dict__:
        AddIce()

def to9():
    if 'firerune' in savedata.__dict__ and 'story_fire' not in savedata.__dict__: 
        system.engine.clearKillQueueCabin()
        cabin.scene('story_fire')      
        system.engine.camera.center()
        system.engine.mapSwitch('map09.ika-map', (system.engine.player.x, 1 * 16), fadeout=False)
    else: 
        system.engine.mapSwitch('map09.ika-map', (system.engine.player.x, 1 * 16))
        
def manaPool():
    if 'firerune' in savedata.__dict__ and ('nearend' not in savedata.__dict__ or 'fireguard' in savedata.__dict__):
        system.engine.player.stats.mp += 1        

def AddIce():
    x=48
    y=416
    e = []
    for i in range(6):
        en = ika.Entity(x + (i* 32), y, system.engine.player.layer, 'ice.ika-sprite')                
        en.name = 'icein10_'+str(i)
        e.append(IceWall(en))                                   
    for en in e:
        system.engine.addEntity(en)   
            
def fightBoss():
    if 'bossin10' not in savedata.__dict__:  
        savedata.bossin10 = 'True'
        y=Yeti(ika.Entity(158, 352, system.engine.player.layer, 'yeti.ika-sprite'))   
        system.engine.addEntity(y)             
        system.engine.mapThings.append(DeathListener(y))
        sound.playMusic("music/competative.xm")    
        sound.yetiDie[0].Play()
        AddIce()


class DeathListener2(Thing):
    'Waits until the yeti is dead, then sets guard to true'
    def __init__(self, yeti=None):
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            sound.playMusic("music/winter.ogg")
            savedata.fireguard = 'True'
            system.engine.addCaptions(Caption('SoulReaver defeated.'))
            return True

    def draw(self):
        pass


class DeathListener(Thing):
    'Waits until the yeti is dead, then stops the music' 
    def __init__(self, yeti=None):
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            sound.playMusic("music/winter.ogg")            
            e = ika.Entity(5*16, 8*16, 2, 'firerune.ika-sprite')
            e.name = 'firerune'
            system.engine.addEntity(FireRune(e))            
            return True

    def draw(self):
        pass

        
class SetupBattle(Thing):
    def update(self):
        sound.playMusic('music/resurrection.it')
        y = SoulReaver(ika.Entity(21*16, 13*16, 3, 'soulreaver.ika-sprite'))
        system.engine.addEntity(y)        
        system.engine.mapThings.append(DeathListener2(y))
        return True

    def draw(self):
        pass
