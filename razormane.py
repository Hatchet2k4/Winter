import ika

from enemy import Enemy
import player
import Brain
import animator
import sound
import math
import system
import dir

_razorManeAnim = {
    'walk': ((
        animator.makeAnim(range(7,14), 9),
        animator.makeAnim(range(14, 21), 9),
        animator.makeAnim(range(21, 28), 9),
        animator.makeAnim(range(0,7), 9),
        animator.makeAnim(range(7,14), 9),
        animator.makeAnim(range(14, 21), 9),
        animator.makeAnim(range(7,14), 9),
        animator.makeAnim(range(14, 21), 9),
        ),
        True
    ),

    'idle': ((
            ((7, 1000),),
            ((14, 1000),),
            ((21, 1000),),
            ((0, 1000),),
            ((7, 1000),),
            ((14, 1000),),
            ((7, 1000),),
            ((14, 1000),),
        ),
        False
    ),

    'attack': ((
        zip(range(35, 37), (30, 20, 15)),
        zip(range(42, 44), (30, 20, 15)),
        zip(range(28, 30), (30, 20, 15)),
        zip(range(49, 51), (30, 20, 15)),
        zip(range(35, 37), (30, 20, 15)),
        zip(range(42, 44), (30, 20, 15)),
        zip(range(35, 37), (30, 20, 15)),
        zip(range(42, 44), (30, 20, 15)),
        ),
        False
    ),

    'hurt': ((
        ((44, 1000),),
        ((37, 1000),),
        ((51, 1000),),
        ((30, 1000),),
        ((44, 1000),),
        ((37, 1000),),
        ((44, 1000),),
        ((37, 1000),),
        ),
        False
    ),

    'die': ((
        ((44, 20),(45, 90)),
        ((37, 20),(38, 90)),
        ((51, 20),(52, 90)),
        ((30, 20),(31, 90)),
        ((44, 20),(45, 90)),
        ((37, 20),(38, 90)),
        ((44, 20),(45, 90)),
        ((37, 20),(38, 90)),
        ),
        False
    ),
}

"""
_attackRange = [
    (-8, 0, 8, 16),
    (16, 0, 8, 16),
    (0, -8, 16, 8),
    (0, 16, 16, 8),
    (-8, 0, 8, 16),
    (16, 0, 8, 16),
    (-8, 0, 8, 16),
    (16, 0, 8, 16),
]
# directions
(LEFT,
 RIGHT,
 UP,
 DOWN,
 UPLEFT,
 UPRIGHT,
 DOWNLEFT,
 DOWNRIGHT,
 NOTHING) = range(9) # coincides with ika's internal direction constants

"""

_attackRange = [
    (-6, 0, 10, 16),
    (18, 0, 10, 16),
    (0, -10, 16, 10),
    (0, 18, 16, 10),
    (-10, 0, 10, 16),
    (18, 0, 10, 16),
    (-10, 0, 10, 16),
    (18, 0, 10, 16),
]

class RazorMane(Enemy):
    def __init__(self, ent):
        Enemy.__init__(self, ent, _razorManeAnim, Brain.Brain())

        self.addMoods(
            (Brain.Attack(1), self.stalkMood),
            (Brain.Flee(1), self.passiveMood)
        )

        self.mood = self.passiveMood
        self.speed = 150
        self.stats.maxhp = self.stats.hp = 50
        self.stats.att = 12
        self.stats.exp = 8      
        self.name='razormane'

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.razorManeHurt.Play()
        #if self.stats.hp < self.stats.maxhp / 2:
        #    self.mood = self.fleeMood
        return super(RazorMane, self).hurtState(recoilSpeed, recoilDir)

    def die(self, *args):
        # When one dies, the others scatter

        ents = [system.engine.entFromEnt[x] for x in
            ika.EntitiesAt(self.x - 60, self.y - 60, 120, 120, self.layer)
            if x in system.engine.entFromEnt]
        allies = filter(lambda e: isinstance(e, RazorMane) and e.stats.hp > 0, ents)

        for a in allies:
            if ika.Random(0, 2) > 0:
                a.mood = a.fleeMood
            else:
                a.mood = a.attackMood #50% chance of more random aggression!
            a.state = a.idleState()

        super(RazorMane, self).die(*args)

    def playerDir(self):
        p = system.engine.player
        return dir.fromDelta(p.x - self.x - 10, p.y - self.y - 7)

    def playerDist(self):
        p = system.engine.player
        return math.hypot(p.x - self.x - 10, p.y - self.y - 7)

    def attackMood(self):
        for q in range(ika.Random(3, 6)):
            d = self.playerDir()
            dist = self.playerDist()
            if dist <= 48:
                yield self.attackState(d)
                yield self.idleState(20)
            else:
                r= ika.Random(0,8)
                if r>=6:                     
                    yield self.walkState(dir.rotateCounterCW[d], min(30, dist))                    
                elif r>=4:
                    yield self.walkState(dir.rotateCW[d], min(30, dist))                        
                else:                       
                    yield self.walkState(d, min(30, dist))



    def stalkMood(self):
        DIST = 0
        p = system.engine.player
        # be DIST away, if at all possible
        while True:
            d = self.playerDir()
            dist = self.playerDist()
            self.direction=d

            if dist - DIST > 48:
                # get closer
                n = int(dist - DIST - 1)
                r= ika.Random(0,8)
                if r>=6:                                        
                    yield self.walkState(dir.rotateCounterCW45[d], ika.Random(int(n / 2), n))                    
                elif r>=4:                    
                    yield self.walkState(dir.rotateCW45[d], ika.Random(int(n / 2), n))                                                        
                yield self.walkState(d, ika.Random(int(n / 2), n))

                yield self.idleState(30)
            elif dist < DIST:
                # fall back
                yield self.walkState(dir.invert[d], min(80, DIST - dist))
                self.direction = dir.invert[d]
                yield self.idleState(30)
            else:
                self.mood = self.attackMood
                yield self.idleState(1)

    def fleeMood(self):
        MIN_DIST = 96
        for q in range(4):
            d = self.playerDir()
            dist = self.playerDist()

            if dist > MIN_DIST:
                break

            yield self.walkState(dir.invert[d], MIN_DIST - dist)

        self.mood = self.passiveMood
        yield self.idleState()

    def passiveMood(self):
        p = system.engine.player
        self._animator.kill = True
        while True:
            dist = self.playerDist()

            yield self.idleState()

            if dist < 192:
                self.mood = self.stalkMood
                yield self.idleState()
                break


    def idleState(self, *args):
        self._animator.kill = True
        return super(RazorMane, self).idleState(*args)

    def walkState(self, dir, dist):
        ox, oy = self.x, self.y
        self.move(dir, dist)
        self.anim = 'walk'
        dist *= 100
        while dist > 0:
            dist -= self.speed
            yield None
            if (ox, oy) == (self.x, self.y):
                break

        self.stop()

    def deathState(self, *args, **kwargs):
        sound.razorManeDie.Play()
        self.anim = 'die'        
        return super(RazorMane, self).deathState(*args, **kwargs)

    def attackState(self, dir):
        class SpeedSaver(object):
            def __init__(_self): _self.s = self.speed
            def __del__(_self):  self.speed = _self.s
        ss = SpeedSaver()

        self.direction = dir
        self.anim = 'attack'
        self.stop()

        sound.razorManeStrike.Play()

        self.speed *= 2

        # Winding up for the pounce.  Stop until the animation advances to the
        # next frame.
        while self._animator.index == 0:
            yield None

        self.move(dir, 32)
        while not self._animator.kill:
            ents = self.detectCollision(_attackRange[dir])

            for e in ents:
                if isinstance(e, player.Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, self.direction)
                    yield None
                    return

            yield None
        self.stop()
