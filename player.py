import ika

import system
import animator
import controls
import sound
import dir
import savedata

from gameover import GameOverException
from statset import StatSet
from caption import Caption, DamageCaption, BGRect
from savepoint import SavePoint
from entity import Entity
from enemy import Enemy
from obstacle import IceWall, IceChunks, Gap, _Obstacle, Crystal
from effects import Nova, Bolt
from serpent import Serpent
from xi import gui

PLAYER_SPRITE = 'protagonist.ika-sprite'
SLASH_LEVEL = 3
BACK_LEVEL = 6
THRUST_LEVEL = 9




# one entry for each direction
_playerAnim = {
    'walk' : ((
        animator.makeAnim(range(28, 36), 8),
        animator.makeAnim(range(19, 27), 8),
        animator.makeAnim(range(10, 18), 8),
        animator.makeAnim(range(1, 9), 8),
        animator.makeAnim(range(28, 36), 8),
        animator.makeAnim(range(19, 27), 8),
        animator.makeAnim(range(28, 36), 8),
        animator.makeAnim(range(19, 27), 8),
        ),
        True
    ),

    'slash': ((
        zip(range(63,68), (8,6,4,2,8)),
        zip(range(54,59), (8,6,4,2,8)),
        zip(range(45,50), (8,6,4,2,8)),
        zip(range(36,41), (8,6,4,2,8)),
        zip(range(63,68), (8,6,4,2,8)),
        zip(range(54,59), (8,6,4,2,8)),
        zip(range(63,68), (8,6,4,2,8)),
        zip(range(54,59), (8,6,4,2,8)),
        ),
        False
    ),

    'backslash': ((
        zip(range(67, 62, -1), (8,6,4,2,8)),
        zip(range(58, 53, -1), (8,6,4,2,8)),
        zip(range(49, 44, -1), (8,6,4,2,8)),
        zip(range(40, 35, -1), (8,6,4,2,8)),
        zip(range(67, 62, -1), (8,6,4,2,8)),
        zip(range(58, 53, -1), (8,6,4,2,8)),
        zip(range(67, 62, -1), (8,6,4,2,8)),
        zip(range(58, 53, -1), (8,6,4,2,8)),
        ),
        False
    ),

    'thrust': ((
        zip((67, 66, 65), (6, 4, 1000)),
        zip((58, 57, 56), (6, 4, 1000)),
        zip((49, 48, 47), (6, 4, 1000)),
        zip((40, 39, 38), (6, 4, 1000)),
        zip((67, 66, 65), (6, 4, 1000)),
        zip((58, 57, 56), (6, 4, 1000)),
        zip((67, 66, 65), (6, 4, 1000)),
        zip((58, 57, 56), (6, 4, 1000)),
        ),
        False
    ),

    'backthrust': ((
        #((90, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        #((72, 1000),),
        ((81, 1000),),
        ((72, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        ),
        True
    ),

    'rend': ((
        zip(range(63,68), (12,8,6,2,12)),
        zip(range(54,59), (12,8,6,2,12)),
        zip(range(45,50), (12,8,6,2,12)),
        zip(range(36,41), (12,8,6,2,12)),
        zip(range(63,68), (12,8,6,2,12)),
        zip(range(54,59), (12,8,6,2,12)),
        zip(range(63,68), (12,8,6,2,12)),
        zip(range(54,59), (12,8,6,2,12)),
        ),
        False
    ),

    'stand': ((
        ((27, 1000),),
        ((18, 1000),),
        ((9, 1000),),
        ((0, 1000),),
        ((27, 1000),),
        ((18, 1000),),
        ((27, 1000),),
        ((18, 1000),)
        ),
        True
    ),

    'hurt': ((
        ((90, 1000),),
        ((99, 1000),),
        ((72, 1000),),
        ((81, 1000),),
        ((90, 1000),),
        ((99, 1000),),
        ((90, 1000),),
        ((99, 1000),),
        ),
        True
    ),

    'die': ((
        zip((90,  91,  92), (20, 20, 1000)),
        zip((99, 100, 101), (20, 20, 1000)),
        zip((72,  73,  74), (20, 20, 1000)),
        zip((81,  82,  83), (20, 20, 1000)),
        zip((90,  91,  92), (20, 20, 1000)),
        zip((99, 100, 101), (20, 20, 1000)),
        zip((90,  91,  92), (20, 20, 1000)),
        zip((99, 100, 101), (20, 20, 1000)),
        ),
        False
    ),

    # temporary:  copy the normal standing frames.
    'magic': ((
        ((27, 1000),),
        ((18, 1000),),
        ((9, 1000),),
        ((0, 1000),),
        ((27, 1000),),
        ((18, 1000),),
        ((27, 1000),),
        ((18, 1000),)
        ),
        True
    ),
}

thrustRange = (
    (-22,  -2, 16, 8),
    ( 15,  -2, 16, 8),
    (  6, -27, 10, 27),
    (  6,  17, 10, 12),
    (-22,  -2, 16, 8),
    ( 15,  -2, 16, 8),
    (-22,  -2, 16, 8),
    ( 15,  -2, 16, 8),
)

slashRange = (
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8), (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8), ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
    ((-14, -27, 10, 27), ( -4, -27, 10, 27), (  6, -27, 10, 27), ( 16, -27, 10, 27), ( 16, -27, 10, 27)),
    (( 16,  17, 10, 12), ( 16,  17, 10, 12), (  6,  17, 10, 12), ( -4,  17, 10, 12), (-14,  17, 10, 12)),
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8), (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8), ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8), (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8), ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
)

rendRange = (
    ((-22, -14, 16,  8), (-24,  -8, 18,  8), (-26,  -2, 20,  8), (-24,   4, 18,  8), (-22,  10, 16,  8)),
    (( 15, -14, 16,  8), ( 15,  -8, 18,  8), ( 15,  -2, 20,  8), ( 15,   4, 18,  8), ( 15,  10, 16,  8)),

    ((-14, -29, 10, 29), ( -4, -29, 10, 29), (  6, -29, 10, 29), ( 16, -29, 10, 29), ( 16, -29, 10, 29)),
    (( 16,  17, 10, 16), ( 16,  17, 10, 16), (  6,  17, 10, 16), ( -4,  17, 10, 16), (-14,  17, 10, 16)),

    ((-22, -14, 16,  8), (-24,  -8, 18,  8), (-26,  -2, 20,  8), (-24,   4, 18,  8), (-22,  10, 16,  8)),
    (( 15, -14, 16,  8), ( 15,  -8, 18,  8), ( 15,  -2, 20,  8), ( 15,   4, 18,  8), ( 15,  10, 16,  8)),

    ((-22, -14, 16,  8), (-24,  -8, 18,  8), (-26,  -2, 20,  8), (-24,   4, 18,  8), (-22,  10, 16,  8)),
    (( 15, -14, 16,  8), ( 15,  -8, 18,  8), ( 15,  -2, 20,  8), ( 15,   4, 18,  8), ( 15,  10, 16,  8)),
)

galeRange = (
    (-17, -8, 8, 24),
    (15, -8, 8, 24),
    (-8, -8, 24, 8),
    (-8, 16, 24, 8),
    (-17, -8, 8, 24),
    (15, -8, 8, 24),
    (-17, -8, 8, 24),
    (15, -8, 8, 24),
)

backSlashRange = [x[::-1] for x in slashRange]

initialStats = StatSet(
    maxhp=120,
    hp=120,
    maxmp=80,
    mp=80,
    att=5,
    mag=5,
    pres=1,
    mres=1,
    level=1,
    exp=0,
    next=10,
    damageind=1,
    tnt=0,    
    guardrunes=0,
    strengthrunes=0,
    powerrunes=0,
    totaltnt=0,
    #kill stats
    anklebiter=0,    
    devourer=0,   
    carnivore=0,    
    razormane=0,    
    dragonpup=0,
    hellhound=0,
    yeti=0,
    gorilla=0,
    soulreaver=0,
    serpent=0    
    )

class Player(Entity):
    def __init__(self, x=0, y=0, layer=0):
        Entity.__init__(self, ika.Entity(x, y, layer, PLAYER_SPRITE), _playerAnim)
        self.state = self.standState()
        self.stats = initialStats.clone()
        self.mptimer = 0
        self.scened = 0

    def giveXP(self, amount):
        self.stats.exp += int(amount * 2) #hack to give more exp because I'm lazy and hate grinding
        if self.stats.exp >= self.stats.next:
            self.levelUp()        

    def levelUp(self):
        sound.achievement.Play()        

        while self.stats.exp >= self.stats.next:
            lev5 = int(self.stats.level / 5)
            
            #every 5 levels, increase potential hp gain
            hpup = ika.Random(2, 4 + lev5) + (lev5*2)
            mpup = ika.Random(1, 4 + lev5) + lev5
            
            self.stats.maxhp += hpup
            self.stats.maxmp += mpup

            statlist = ['att', 'mag', 'pres']
            
            statsup = {'att':0, 'mag':0, 'pres':0}
            statnames = {'att':'Attack', 'mag':'Magic', 'pres':'Defense'}
            
            statpoints = 1 
            if lev5>0: statpoints+=ika.Random(0, lev5+1) #every 5 levels, potentially gain another stat point           
            
            for n in range(statpoints):
                #random chance of any stat increase. 
                s = statlist[ika.Random(0,len(statlist))] 
                self.stats[s]+= 1
                statsup[s]+=1
            
            self.stats.level += 1

            self.stats.maxhp = min(self.stats.maxhp, 285)
            self.stats.maxmp = min(self.stats.maxmp, 285)
            self.stats.exp -= self.stats.next
            self.stats.next = self.stats.level * (self.stats.level + 1) * 5

        d = 300
        starty=165

        shade=100
        red=250
        green=200
        blue=30
        appendlist=[]        
        
        appendlist.append(Caption('Level %i!' % self.stats.level, y=starty, duration=d, r=red,g=green,b=blue))
        if self.stats.maxhp==285:
            appendlist.append(Caption('HP Maxed!', y=starty+10, duration=d,  r=red,g=green,b=blue))
        else:
            appendlist.append(Caption('HP +%i' % hpup, y=starty+10, duration=d,  r=red,g=green,b=blue))
        if self.stats.maxmp==285:
            appendlist.append(Caption('MP Maxed!', y=starty+10, duration=d,  r=red,g=green,b=blue))
        else:    
            appendlist.append(Caption('MP +%i' % mpup, y=starty+20, duration=d,  r=red,g=green,b=blue))
            
        i=0
        numlines=3
        bgw = gui.default_font.StringWidth('Level %i!' % self.stats.level)              
        for s in statlist:
            if statsup[s]:
                appendlist.append(Caption(statnames[s] +' +%i' % statsup[s], y=starty+30 + (10*i), duration=d, r=red,g=green,b=blue))
                bgw = max(gui.default_font.StringWidth(statnames[s] +' +%i' % statsup[s]), bgw)
                numlines+=1
                i+=1

        bgw+=8
        bgh = (numlines)*10 + 6
        bgx = 160-(bgw/2)
        bgy = starty-4                
        #appendlist = [BGRect(bgx,bgy,bgw,bgh, duration=d)]+appendlist
        system.engine.addCaptions(appendlist)                        
        
        appendlist = []        
        line1=line2=''        
        if self.stats.level in [SLASH_LEVEL, BACK_LEVEL, THRUST_LEVEL]:      
            if self.stats.level == SLASH_LEVEL: 
                line1= 'Slash skill learned!'
                line2= 'Press attack twice to combo.'
            elif self.stats.level == BACK_LEVEL: 
                line1= 'Backdash skill learned!'
                line2= 'Press opposite direction after attacking.'
            elif self.stats.level == THRUST_LEVEL: 
                line1= 'Thrust skill learned!'
                line2= 'Attack again a moment after a slash.'                                        
            appendlist.append(Caption(line1, y=starty, duration=d, r=red,g=green,b=blue))
            appendlist.append(Caption(line2, y=starty+10, duration=d, r=red,g=green,b=blue))            
            
            bgw = gui.default_font.StringWidth(line2) + 8
            bgh = 21 + 4
            bgx = 160-(bgw/2)
            #bgy = starty-2                
            #appendlist = [BGRect(bgx,bgy,bgw,bgh, delay=d+150, duration=d)]+appendlist
            system.engine.addCaptions(appendlist)    


    def calcSpells(self):
        '''
        Figures out what spells the player has access to, based on the
        flags set in the savedata module.
        '''
        bind = len([x for x in savedata.__dict__.keys() if x.startswith('bind')])
        self.stats.rend = 'firerune' in savedata.__dict__
        self.stats.heal = 'waterrune' in savedata.__dict__
        self.stats.gale = 'windrune' in savedata.__dict__
        self.stats.bolt = 'unityrune' in savedata.__dict__

    def regenMP(self):
        if self.stats.mp < self.stats.maxmp:
            self.mptimer+=1
            if self.mptimer >= 200:
                self.mptimer = 0
                self.stats.mp+=1 + int(self.stats.mag / 10)
                
    def defaultState(self):
        return self.standState()

    def standState(self):
        self.stop()
        self.anim = 'stand'
            
        while True:
            self.regenMP()        
            if controls.attack() or controls.joy_attack():
                self.state = self.slashState()
            elif controls.rend() or controls.joy_rend():
                self.state = self.hearthRendState()
                yield None
            elif controls.gale() or controls.joy_gale():
                self.state = self.crushingGaleState()
                yield None
            elif controls.heal() or controls.joy_heal():
                self.state = self.healingRainState()
                yield None
            elif controls.bolt() or controls.joy_bolt():
                self.state = self.boltState()
                yield None
            elif controls.left() or controls.right() or controls.up() or controls.down() or controls.joy_left() or controls.joy_right() or controls.joy_up() or controls.joy_down():
                self.state = self.walkState()
                self._state() # get the walk state started right now.
            yield None

    def walkState(self):
        oldDir = self.direction
        self.anim = 'walk'
        while True:
            self.regenMP()                
            if controls.attack() or controls.joy_attack():
                self.state = self.slashState()
            elif controls.rend() or controls.joy_rend():
                self.state = self.hearthRendState()
                yield None
            elif controls.gale() or controls.joy_gale():
                self.state = self.crushingGaleState()
                yield None
            elif controls.heal() or controls.joy_heal():
                self.state = self.healingRainState()
                yield None
            elif controls.bolt() or controls.joy_bolt():
                self.state = self.boltState()
                yield None                
            elif controls.left() or controls.joy_left():
                if controls.up()  or controls.joy_up():
                    d = dir.UPLEFT
                elif controls.down()  or controls.joy_down():
                    d = dir.DOWNLEFT
                else:
                    d = dir.LEFT
            elif controls.right() or controls.joy_right():
                if controls.up() or controls.joy_up():
                    d = dir.UPRIGHT
                elif controls.down() or controls.joy_down():
                    d = dir.DOWNRIGHT
                else:
                    d = dir.RIGHT
            elif controls.up() or controls.joy_up():
                d = dir.UP
            elif controls.down() or controls.joy_down():
                d = dir.DOWN
            else:
                self.state = self.standState()
                yield None

            self.move(d)

            # handle animation and junk
            if d != oldDir:
                self.anim = 'walk'
                self.direction = d
                oldDir = d
            yield None           
            
    def cutsceneWalkState(self):
        oldDir = self.direction
        self.anim = 'walk'
        while True:            
            self.move(self.direction)

            # handle animation and junk
            if self.direction != oldDir:
                self.anim = 'walk'
                self.direction = d
                oldDir = d
            yield None   

    def cutsceneStandState(self):

        self.anim = 'stand'
        while True:            
            yield None            

    def slashState(self):
        self.stop()
        self.anim = 'slash'
        r = slashRange[self.direction]
        backslash = False
        backthrust = False

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.slash1.Play()

        while not self._animator.kill:
            rect = list(r[self._animator.index]) + [self.layer]
            rect[0] += self.x
            rect[1] += self.y
            ents = ika.EntitiesAt(*rect)
            for e in ents:
                x = system.engine.entFromEnt[e]
                if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                    hitList.append(x)
                    x.hurt( int(self.stats.att + ika.Random(0, 3)), 120, self.direction)
                    self.giveMPforHit()
            if self.stats.level >= BACK_LEVEL: 
                if (controls.up() or controls.joy_up()) and self.direction == dir.DOWN:  backthrust = True
                elif (controls.down()  or controls.joy_down()) and self.direction == dir.UP:  backthrust = True
                elif (controls.left() or controls.joy_left()) and self.direction in [dir.RIGHT, dir.UPRIGHT, dir.DOWNRIGHT]:  backthrust = True
                elif (controls.right() or controls.joy_right()) and self.direction in [dir.LEFT, dir.UPLEFT, dir.DOWNLEFT]:  backthrust = True

            if (controls.attack() or controls.joy_attack()) and self.stats.level >= SLASH_LEVEL: 
                backslash = True

            yield None

        if backthrust:
            self.state = self.backThrustState()
            yield None
        elif backslash:
            self.state = self.backSlashState()
            yield None
        else:
            # Stall:
            count = 10
            while count > 0:
                count -= 1
                if self.stats.level >= THRUST_LEVEL and (controls.attack() or controls.joy_attack()):
                    self.state = self.thrustState()
                yield None

    def backSlashState(self):
        self.stop()
        self.anim = 'backslash'
        r = backSlashRange[self.direction]

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.slash2.Play()

        while not self._animator.kill:
            rect = list(r[self._animator.index]) + [self.layer]
            rect[0] += self.x
            rect[1] += self.y
            ents = ika.EntitiesAt(*rect)
            for e in ents:
                x = system.engine.entFromEnt[e]
                if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                    hitList.append(x)
                    x.hurt(int(self.stats.att + ika.Random(0, 3) * 1.25 ), 130, self.direction)
                    self.giveMPforHit()

            yield None

        # Stall:
        count = 10
        while count > 0:
            count -= 1
            if controls.rend() or controls.joy_rend():
                self.state = self.hearthRendState()
            elif self.stats.level >= THRUST_LEVEL and (controls.attack() or controls.joy_attack()):
                self.state = self.thrustState()
            yield None

    def thrustState(self):
        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        class SpeedSaver(object):
            def __init__(_self):        _self.s = self.speed
            def __del__(_self):         self.speed = _self.s

        ss = SpeedSaver()

        self.anim = 'thrust'
        self.speed += 800
        self.move(self.direction, 1000)

        r = thrustRange[self.direction] + (self.layer,)
        rect = list(r)

        sound.slash3.Play()

        # hack since I need to break out of two levels at once
        def thing():
            i = 8
            while i > 0:
                i -= 1
                self.speed -= (12 - i) * 10

                rect[0] = r[0] + self.x
                rect[1] = r[1] + self.y
                ents = ika.EntitiesAt(*rect)
                for e in ents:
                    x = system.engine.entFromEnt[e]
                    if isinstance(x, Enemy) and not x.invincible:
                        x.hurt(int(self.stats.att * 1.5) + ika.Random(0, 4), 300, self.direction)
                        self.giveMPforHit()
                        self.stop()
                        return

                yield None
        for x in thing():
            yield x

        i = 30
        while i > 0:
            i -= 1
            self.speed = max(10, self.speed - 10)
            yield None

        self.stop()

    def backThrustState(self):
        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        class SpeedSaver(object):
            def __init__(_self):        _self.s = self.speed
            def __del__(_self):         self.speed = _self.s

        ss = SpeedSaver()

        self.anim = 'backthrust'
        self.speed += 400
        self.move(dir.invert[self.direction], 1000)
        sound.dodge.Play()

        i = 8
        while i > 0:
            i -= 1
            self.speed -= 40
            yield None

        i = 30
        thrust = False
        gale = False

        while i > 0:
            i -= 1
            self.speed = max(0, self.speed - 10)
            if controls.attack() or controls.joy_attack():
                thrust = True
            elif controls.gale() or controls.joy_gale():
                gale = True
            yield None

        self.direction = dir.invert[self.direction]

        if thrust:
            self.state = self.thrustState()
            yield None

        elif gale:
            self.state = self.crushingGaleState()
            yield None

        self.stop()

    def hearthRendState(self):
        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        self.stop()
        self.anim = 'rend'
        r = rendRange[self.direction]

        if self.stats.mp < 10 or not self.stats.rend:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 10

        # charge
        # TODO: sound/particle effect here
        while self._animator.index == 0:
            yield None

        fire = ika.Entity(self.x, self.y, self.layer, 'rend.ika-sprite')
        f = self.direction * 5 # hack.

        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []

        sound.hearthRend.Play()
        
        self.invincible = True #invincible while swinging, why not!
        while not self._animator.kill:
            ents = self.detectCollision(r[self._animator.index] + (self.layer,))
            fire.specframe = f + self._animator.index

            for e in ents:
                if isinstance(e, Enemy) and not e.invincible and e not in hitList:
                    hitList.append(e)
                    if(isinstance(e, Serpent)): #he resists, no extra 1.5!
                        e.hurt( int( ((self.stats.att + self.stats.mag) + ika.Random(-3, 3))), 300, self.direction)
                    else: 
                        e.hurt(int((self.stats.att + self.stats.mag) * 1.5) + ika.Random(-3, 3), 300, self.direction)
                elif isinstance(e, IceWall):
                    # TODO: some sort of nice animation.
                    setattr(savedata, e.flagName, 'True')

                    system.engine.destroyEntity(e)
                    #system.engine.things.append(Caption('The ice melted!'))

            yield None
        self.invincible = False #no longer invincible during stall period

        del fire

        # stall period:
        for i in range(30):
            yield None

    def crushingGaleState(self):
        class Saver(object):
            def __init__(_self):
                _self.speed = self.speed
                _self.o = self.ent.entobs
                _self.i = self.invincible
                _self.l = system.engine.camera.locked
            def __del__(_self):
                self.speed = _self.speed
                self.ent.entobs = _self.o
                self.invincible = _self.i
                system.engine.camera.locked = _self.l

        saver = Saver()
        

        if self.direction == dir.UPLEFT or self.direction == dir.DOWNLEFT:
            self.direction = dir.LEFT
        elif self.direction == dir.UPRIGHT or self.direction == dir.DOWNRIGHT:
            self.direction = dir.RIGHT

        self.stop()
        self.anim = 'stand'

        if self.stats.mp < 15 or not self.stats.gale:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 15

        camera = system.engine.camera

        camera.locked = True
        dx, dy = dir.delta[self.direction]

        # charge

        sound.crushingGale.Play()

        for i in range(30):
            #ika.Map.xwin += dx 
            #ika.Map.ywin += dy
            yield None

        self.invincible = True
        self.ent.entobs = False

        self.anim = 'thrust'
        r = galeRange[self.direction] + (self.layer,)
        self.move(self.direction, 100000)
        self.speed *= 10
        camera.locked = False
        camera.speedup()
        
        for i in range(60):
            ents = self.detectCollision(r)
            for e in ents:
                if isinstance(e, Enemy) and not e.invincible:
                    e.hurt(int(self.stats.att + self.stats.mag * 1.5) + ika.Random(-4, 8), 300, (self.direction + 2) & 3)
                elif isinstance(e, _Obstacle) or isinstance(e, SavePoint):                  
                    self.stop()
                    self.state = self.standState()

            yield None
            self.speed = max(saver.speed, self.speed - 20)

        while True:
            ents = [x for x in self.detectCollision((0, 0, self.ent.hotwidth, self.ent.hotheight, self.layer)) if isinstance(x, Gap)]
            if not ents:
                break
            else:
                yield None

        self.stop()



    def healingRainState(self):
        self.stop()
        self.anim = 'magic'

        if self.stats.mp < 15 or not self.stats.heal:
            sound.menuBuzz.Play()
            return

        self.stats.mp -= 15
        sound.healingRain.Play()

        duration=45

        x = self.ent.x + (self.ent.hotwidth / 2)
        y = self.ent.y
        system.engine.addThing(Nova(x, y, 1.0, duration, speed=0.5, color = ika.RGB(0, 120, 240, 255), filled=True ))
        system.engine.addThing(Nova(x, y, 2.0, duration, speed=0.4, color = ika.RGB(100, 200, 255, 255), filled=False ))
        system.engine.addThing(Nova(x, y, 2.0, duration, speed=0.25, color = ika.RGB(200, 200, 255, 255), filled=True ))
        system.engine.addThing(Nova(x, y, 4.0, duration-5, speed=0.6, color = ika.RGB(0, 0, 200, 255), filled=False ))

        self.invincible = True


        amount = self.stats.mag + self.stats.maxhp/8 + ika.Random(-3, 6) #minimum ~12.5% heal        
        self.stats.hp += amount
               
        if self.stats.damageind:
            x=self.ent.x + self.ent.hotwidth/2 - gui.default_font.StringWidth(str(amount))/2
            y=self.ent.y 
            system.engine.addThing(DamageCaption(str(amount), x, y, 40, 0, 240, 60))
            
            
        ents = self.detectCollision((-20, -20, 36, 36, self.layer))

        for e in ents:
            if isinstance(e, IceChunks):
                e.freeze()
                #system.engine.addCaptions(Caption('The water froze over!'))
                system.engine.destroyEntity(e)
                break

        for i in range(duration):
            yield None

        self.invincible = False

    def smokeScreenState(self):
        pass

    def boltState(self):
        self.stop()
        self.anim = 'thrust'
        costperhit=6
        
        if self.stats.mp < costperhit or not self.stats.bolt:
            sound.menuBuzz.Play()
            return

        for i in range(8): #8 cycle delay before attack starts
            yield None
        offsetx = offsety = 0
        
        #hack, should use a dict but lazy
        if self.direction == dir.DOWN:
            offsetx=8
            offsety=30
        elif self.direction == dir.UP:
            offsetx=5
            offsety=-25
        elif self.direction in [dir.RIGHT, dir.UPRIGHT, dir.DOWNRIGHT]:  
            offsetx=34
            offsety=-2
        elif self.direction in [dir.LEFT, dir.UPLEFT, dir.DOWNLEFT]: 
            offsetx=-24
            offsety=-2            
            
        ents = self.detectCollision((
           -96, -96, 192, 192, self.layer
            ))
        
        #costmp=False
            
        self.invincible=True
        destroyents = []
        n=0
        for e in ents:
            if e and (isinstance(e, Enemy) and not e.invincible) or isinstance(e, IceWall) or isinstance(e, Crystal):
                if self.stats.mp>=costperhit: 
                    self.stats.mp -= costperhit
                else:
                    sound.menuBuzz.Play()
                    break
                    
                #if not costmp:                    
                #    costmp=True
                #    self.stats.mp -= costperhit 
                                               
                if isinstance(e, Enemy):
                    d = dir.invert[dir.fromDelta(self.x - e.x, self.y - e.y)]
                    if(isinstance(e, Serpent)): #he resists, half damage to prevent bolt spam!
                        e.hurt( int( ((self.stats.att + self.stats.mag) + ika.Random(1, int(self.stats.mag))) / 2), 300, d)
                    else:
                        e.hurt(int(self.stats.att + self.stats.mag) + ika.Random(1, int(self.stats.mag)), 300, d)
                elif isinstance(e, IceWall) or isinstance(e, Crystal):
                    setattr(savedata, e.flagName, 'True')                    
                    destroyents.append(e)                    
                system.engine.addThing(Bolt(self.x+offsetx, self.y+offsety, 
                                            e.x+(e.ent.hotwidth/2), e.y+(e.ent.hotheight/2), ika.RGB(240,40,128) ))
                system.engine.addThing(Nova(self.x+offsetx, self.y+offsety, 0.5, 24, speed=0.5, color = ika.RGB(240, 100, 128, 255), filled=True ))                                            
                system.engine.addThing(Nova(e.x+(e.ent.hotwidth/2), e.y+(e.ent.hotheight/2), 0.5, 24, speed=0.5, color = ika.RGB(240, 100, 128, 255), filled=True ))                                            
                 
                #if n % 3==0:
                #sound.boltStorm.StopAllSounds()
                sound.boltStorm.Play()  #only play sound every 4 to minimize noise                                          
                n+=1    
                
                for i in range(5): #wait a few frames before attacking next enemy
                    yield None
        
        for e in destroyents:
            system.engine.destroyEntity(e)
        

        self.stop()
        self.invincible=False
        for i in range(40):
            yield None

        #if costmp: # continue stall only if there were enemies in range
        #    for i in range(40):
        #        yield None

    def vivifyState(self):
        pass

    def ternionState(self):
        pass

    def die(self):
        self.state = self.deathState()
        self._state()
        self.anim = 'die'
        raise GameOverException()

    def deathState(self):
        self.invincible = True
        s = self.hurtState(300, dir.invert[self.direction])
        yield s.next()
        self.anim = 'die'
        for x in s:
            yield None

        while True:
            yield None

    def giveMPforHit(self):
        #self.stats.mp += ika.Random(0,2 + (self.stats.level/5) ) 
        pass