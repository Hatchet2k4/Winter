import ika
import savedata
import system
import dir
from serpent import Serpent
from thing import Thing
import sound
from caption import Caption

savedata = savedata.__dict__ # fuckit

def AutoExec():
    l = ika.Map.FindLayerByName('B1.5')
    #ika.Map.SetLayerTint(l, ika.RGB(255, 255, 255, 100))
    #ika.Map.SetLayerPosition(l, -1000, -1000) #ice layer not needed yet!
    
# essentially autoExec
def finalBattle():
    if 'finalbattle' in savedata:
        pass
        # make the river passable
    else:
        savedata['finalbattle'] = 'True'        

        p = system.engine.player        
        
        def walkUp():
            p.move(dir.UP, 96)
            p.anim = 'walk'
            for n in range(96):
                yield None

        p.state = walkUp()

        for n in range(96):
            system.engine.tick()
            system.engine.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

        def noOp():
            while True:
                yield None

        p.anim = 'stand'
        p.state = noOp()

        for n in range(256):
            # teh earthquake
            ika.Map.xwin += ika.Random(-4, 5)
            ika.Map.ywin += ika.Random(-4, 5)
            system.engine.tick()
            system.engine.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

        s = Serpent(
            ika.Entity(25 * 16, 24 * 16, p.layer, 'serpent.ika-sprite')
            )
        s.anim = 'appear'
        system.engine.addEntity(s)

        for n in range(19, 32):
            # close off the way back
            ika.Map.SetTile(n, 38, p.layer, 26)
            ika.Map.SetTile(n, 39, p.layer, 32)
            ika.Map.SetObs(n, 38, p.layer, True)
            system.engine.tick()
            system.engine.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

        p.state = p.defaultState()

        s.state = s.roarState()
        system.engine.synchTime()
        system.engine.mapThings.append(DeathListener(s))

temp = [145, 149, 149, 149, 144]

icebridge = {
28: [0, 113, 112, 113, 0],
27: [147, 113, 110, 113, 146],
26: [142, 110, 113, 109, 143],
25: [142, 109, 110, 112, 143],
24: [142, 113, 112, 110, 143],
23: [142, 110, 113, 109, 143],
22: [142, 109, 110, 112, 143],
21: [142, 113, 112, 110, 143],
20: [142, 110, 113, 109, 143],
19: [141, 108, 113, 112, 140],
}




class DeathListener(Thing):
    'Waits until the serpent is dead, then starts the credits music and sets the ice to cross'
    def __init__(self, serpent=None):
        self.serpent = serpent
        self.buildbrige = False
        self.time=0
        self.row = 28
        
    def update(self):            
        if self.serpent.stats.hp == 0 and not self.buildbrige:
            sound.playMusic("music/Existing.s3m")  
            sound.achievement.Play()
            system.engine.addCaptions(Caption('Serpent defeated!'))
            savedata['finalbattledone'] = 'True'
            self.buildbrige = True        
            self.time=100:#wait 1 second before starting to build the bridge
        
        if self.buildbrige:
            if self.time==0:                
                self.time = 20
                l = ika.Map.FindLayerByName('B1.5')
                if self.row == 27: 
                    ol = ika.Map.FindLayerByName('B2')
                    for y in range(27, 18, -1): #haaaack
                        if y == 19 or y == 27:
                            obs = [0, 0, 0, 0, 0]
                        else: obs = [1, 0, 0, 0 ,1]
                        for x, o in enumerate(obs):                                                    
                            ika.Map.SetObs(x+21, y, ol, o)
                            
                for x in range(5):                    
                    ika.Map.SetTile(x+21, self.row, l, icebridge[self.row][x])
                    if self.row>19:
                        ika.Map.SetTile(x+21, self.row-1, l, temp[x])                                    
                self.row-=1        
                if self.row<19:
                    return True #done
            else: 
                self.time-=1

            

    def draw(self):
        pass

def to31():
    pass

def to33():
    system.engine.mapSwitch('map33.ika-map', (10 * 16+1, 40 * 16))

