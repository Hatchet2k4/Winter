
import ika
import system
import animator
import Brain
import dir
import ending
import xi.effects
import math
import player

from enemy import Enemy
from carnivore import Carnivore
from anklebiter import AnkleBiter

# arbitrary :D
_idleAnim = animator.makeAnim((0, 4, 0, 0, 0, 4, 0, 0, 1, 2, 3, 2, 1, 0), 50)
_biteAnim = animator.makeAnim(range(16, 22), 7) # could do some speed-tinkering here.  Make the first and last frames slower than the middle ones.
_stareAnim = animator.makeAnim((4, 5, 5, 6, 6, 7, 7, 6, 5, 4, 4), 4)
_roarAnim = animator.makeAnim((12, 13, 13, 14, 15, 16, 16, 16, 14, 12), 20)
_deathAnim = animator.makeAnim(range(24, 27), 100)
_appearAnim = animator.makeAnim((26, 25, 24), 20)
_hurtAnim = ((10, 50),)

_anim = {
    'idle': ((_idleAnim,) * 8, True),
    'bite': ((_biteAnim,) * 8, False),
    'stare': ((_stareAnim,) * 8, False),
    'roar': ((_roarAnim,) * 8, False),
    'die': ((_deathAnim,) * 8, False),
    'appear': ((_appearAnim,) * 8, False),
    'hurt': ((_hurtAnim,) * 8, False),
}

_biteRange = (
    (0, 41, 30, 0),
    (0, 41, 30, 6),
    (0, 41, 30, 20),
    (0, 41, 30, 30),
    (0, 41, 30, 0),
    (0, 41, 30, 0),
)

class Serpent(Enemy):
    def __init__(self, ent):
        Enemy.__init__(self, ent, _anim, Brain.Brain())

        self.addMoods(
            (Brain.Attack(1), self.watchMood)
            )

        self.stats.maxhp = 300 #must bump up before release!
        self.stats.hp = self.stats.maxhp
        self.stats.att = 40
        self.invincible = True
        
        self.name='serpent'
        ent.mapobs = ent.entobs = False
        self.bleh = self.watchMood()
        

    def die(self):
        xi.effects.fadeOut(200, draw=system.engine.draw)
        ending.credits()

    def think(self):
        self.state = self.bleh.next()

    def hurt(self, amount, speed = 0, dir = None):
        Enemy.hurt(self, amount, 0, dir)

    def hurtState(self, *args):
        self.anim = 'hurt'
        self.invincible = True
        self.interruptable = False
        i = 30
        while i > 0:
            i -= 1
            yield None

        self.interruptable = True

    def watchMood(self):
        '''
        Go left to right, try to vertically align with the player,
        then try to bite.
        Roar every now and again.
        '''
        p = system.engine.player

        while True:
            # why is this necessary? O_o
            #self.interruptable = True
            #self._state = None

            for n in range(ika.Random(1, 8)):
                x = self.x + self.ent.hotwidth / 2
                d = dir.fromDelta(p.x - x, 0)
                yield self.moveState(d, abs(p.x - x))

                c = ika.Random(0, 100) 
                if c < 35:
                    yield self.biteState()
                elif c < 75: 
                    yield self.stareState()
                
            yield self.roarState()

    def moveState(self, dir, dist):
        self.anim = 'idle'
        self.move(dir, dist)

        dist *= 100
        while dist > 0:
            dist -= self.speed
            yield None

    def biteState(self):
        self.anim = 'bite'
        self.invincible = False

        while not self._animator.kill:
            r = _biteRange[self._animator.index] + (self.layer,)
            ents = self.detectCollision(r)
            for e in ents:
                d = max(1, self.stats.att - system.engine.player.stats.pres)
                e.hurt(d, 350, dir.DOWN)
            yield None

        for i in range(60):
            yield None

        self.invincible = True

    def stareState(self):
        self.anim = 'stare'
        self.invincible = False
        e = Beam(ika.Entity(self.x+8, self.y-8, self.layer, 'beam.ika-sprite'))
        system.engine.addEntity(e)
        
        while not self._animator.kill:
            yield None
        
        self.invincible = True
        # TODO: finish this if someone can think of a good idea for
        # what it should do!
        
        #stole from Mannux
        #dx = self.x - engine.player.x - engine.player.width / 2 + 8
        #dy = self.y - engine.player.y - engine.player.height / 2 + 8
        #angle = math.atan2(dy, dx) + math.pi
        #engine.AddEntity(Laser(self.x + 8, self.y + 8, angle, self))
        

    def roarState(self):
        # spawn one to five Carnivores to irritate the shit out of the player
        self.anim = 'roar'
        s = False

        for wait in range(200):
            n = self._animator.curFrame - 12 # Yet another gay hack.
            ika.Map.xwin += ika.Random(-n, n + 1)
            ika.Map.ywin += ika.Random(-n, n + 1)
            yield None

        for q in range(ika.Random(1, 4)):
            x, y = 320 + (q * 60), 588
            n = ika.EntitiesAt(x, y, x + 16, y + 16, self.layer)

            if not n:
                if ika.Random(0, 2):
                    e = Carnivore(ika.Entity(x, y, self.layer, 'carnivore.ika-sprite'))
                else:
                    e = AnkleBiter(ika.Entity(x, y, self.layer, 'anklebiter.ika-sprite'))
                system.engine.addEntity(e)
                e.mood = e.attackMood

        # need to destroy old corpses (a first!)
        for e in system.engine.entities:
            if e.stats.hp == 0 and isinstance(e, Enemy):
                system.engine.destroyEntity(e)

        while not self._animator.kill:
            n = self._animator.curFrame - 12
            ika.Map.xwin += ika.Random(-n, n + 1)
            ika.Map.ywin += ika.Random(-n, n + 1)
            yield None


flyAnim = animator.makeAnim(range(10), 10)  

_beamanim = {
    'flyAnim': ((flyAnim,) * 8, False),
    'idle': ((flyAnim,) * 8, True),
    'die': ((flyAnim,) * 8, False),
    'hurt': ((flyAnim,) * 8, False),
}
class Beam(Enemy):
    def __init__(self, ent):
        Enemy.__init__(self, ent, _beamanim, Brain.Brain())

        flyAnim = animator.makeAnim(range(10), 10)   
        
        self.addMoods(
            (Brain.Attack(1), self.flyMood)
            )

        self.stats.maxhp = 10
        self.stats.hp = self.stats.maxhp
        self.stats.att = 35
        self.invincible = True
        
        self.anim =  'flyAnim'
        
        self.name='beam'
        ent.mapobs = ent.entobs = False
        self.bleh = self.flyMood()
        
        p = system.engine.player
        
        self.x=self.ent.x
        self.y=self.ent.y
        
        dx = (self.x - 8) - (p.x + 7)
        dy = (self.y - 8) - (p.y + 8)
        self.angle = math.atan2(dy, dx) + math.pi        

    def think(self):
        self.state = self.bleh.next()
        
    def flyMood(self):    
            yield self.flyState()               
    

    def flyState(self):        
        self.direction=dir.DOWN
        while not self._animator.kill:
            self.x += 3 * math.cos(self.angle)
            self.y += 3 * math.sin(self.angle)
            ents = self.detectCollision((0,0,16,16))
            
            for e in ents:
                if isinstance(e, player.Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, self.direction)
                    self.die()
                    self.x=self.y=-1000
                    yield None
                    return
            yield None        
        self.x=self.y=-1000
        self.die()
        yield None
    