import ika
import system
import savedata
import sound
from thing import Thing
from yeti import Yeti
from soulreaver import SoulReaver
from razormane import RazorMane
from rune import WaterRune
from snow import Snow
import cabin

def AutoExec():
    system.engine.mapThings.append(Snow(6000, velocity=(-.2, 3)))
    if 'waterrune' not in savedata.__dict__:
        system.engine.things.append(RuneListener())
    if 'nearend' in savedata.__dict__:
        system.engine.things.append(RuneListener())
    if 'icechunks1' in savedata.__dict__:
        breakIceRun()
    sound.playMusic("music/wind.ogg")

        

def to3():
    offset_from = 11 * 16  # first horizontal pos possible
    offset_to = 8 * 16  # first horizontal pos possible
    x = system.engine.player.x - offset_from + offset_to
    system.engine.mapSwitch('map03.ika-map', (x, 1 * 16))

def to5():
    system.engine.mapSwitch('map05.ika-map', (10 * 16, 19 * 16))

def breakIce():
    if not 'brokeice' in savedata.__dict__:        
        breakIceRun()
        sound.healingRain.Play()
        setattr(savedata, 'brokeice', 'True')
        

def breakIceRun():
    for x in range(13, 18):
        for y in range(33,37):
            ika.Map.SetTile(x, y, 3, 0)
            if x in (13, 17) and y > 33: ika.Map.SetObs(x, y, 4, 1)
                
    ika.Map.entities['icechunks1'].layer = 3

def story04():
    if 'waterrune' in savedata.__dict__ and 'story_4' not in savedata.__dict__: 
      cabin.scene('story_4')
      system.engine.camera.center()
      

def spawnpack():
    if 'waterrune' not in savedata.__dict__ and 'pack' not in savedata.__dict__:      
        savedata.pack = 'True' 
        e = [
        RazorMane(ika.Entity(15* 16, 29 * 16, system.engine.player.layer, 'razormane.ika-sprite')),
        RazorMane(ika.Entity(11* 16, 31 * 16, system.engine.player.layer, 'razormane.ika-sprite')),
        RazorMane(ika.Entity(19* 16, 29 * 16, system.engine.player.layer, 'razormane.ika-sprite'))
        ]
        for en in e:
            system.engine.addEntity(en)                
        system.engine.mapThings.append(DeathListener(e))
        sound.playMusic("music/competative.xm")    
        sound.razorManeStrike.Play()
        


class DeathListener(Thing): #for initial wolves battle
    def __init__(self, e=None):
        self.enemies = e

    def update(self):
        done = True
        for e in self.enemies:
            if e.stats.hp > 0:
                done = False
        if done: #all are dead
            sound.playMusic("music/wind.ogg")
            e = ika.Entity(245, 262, 4, 'waterrune.ika-sprite')
            e.name = 'waterrune'
            system.engine.addEntity(WaterRune(e))                                    
            return True

    def draw(self):
        pass
        
class DeathListener2(Thing): #for SoulReaver quest

    def __init__(self, yeti=None):
        self.yeti = yeti

    def update(self):
        if self.yeti.stats.hp == 0:
            sound.playMusic("music/wind.ogg")
            savedata.waterguard = 'True'
            return True

    def draw(self):
        pass
        
class RuneListener(object):
    def update(self):
        if 'nearend' in savedata.__dict__ and 'waterguard' not in savedata.__dict__:
            sound.playMusic("music/resurrection.it")
            y = SoulReaver(ika.Entity(15* 16, 17 * 16, system.engine.player.layer, 'soulreaver.ika-sprite'))
            system.engine.addEntity(y)
            system.engine.mapThings.append(DeathListener2(y))
            return True


    def draw(self):
        pass
