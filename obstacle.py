'''Contains entities that are obstructions in the player's path.
Given the proper skill or item, the player can cross these.
'''

import ika
import savedata
import system
import automap
import sound

from entity import Entity
from caption import Caption

class _Obstacle(Entity):
    def __init__(self, ent, anim = None):
        self.flagName = ent.name
        Entity.__init__(self, ent, anim)
        self.invincible = True
        print self.flagName + ' inited'    

        if self.flagName in savedata.__dict__:
            #print 'Removed ' + self.flagName
            self.remove()
            

    def remove(self):
        self.x = self.y = -100
        system.engine.destroyEntity(self)

    def update(self):
        pass

class _GapObstacle(Entity):
    def __init__(self, ent, anim = None):
        self.flagName = ent.name
        Entity.__init__(self, ent, anim)
        self.invincible = True

        if self.flagName in savedata.__dict__:
            self.remove()

    def remove(self):
        self.x = self.y = -100
        system.engine.destroyEntity(self)

    def update(self):
        pass

class IceWall(_Obstacle):
    '''
    Not very exciting.  The entity's type is all the information
    we need.
    '''
    pass

class Crystal(_Obstacle):
    '''
    Not very exciting.  The entity's type is all the information
    we need.
    '''
    def remove(self):
        self.x = self.y = -100
        system.engine.destroyEntity(self)       
        e = ika.Entity(self.x-16, self.y-8, self.ent.layer+1, 'explosion.ika-sprite')
        system.engine.addEntity(Explosion(e))

class Gap(_GapObstacle): #inheriting from different class in order to handle gaps differently
    '''A big empty hole. :P'''
    pass

class IceChunks(_Obstacle):
    _anim = {
        'default': ((
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ((0, 50),(1, 50),),
            ),
            True
        )
    }

    _frozenTiles = (
        (145, 149, 144),
        (142, 113, 143),
        (139, 148, 138)
    ) #tiles to fill in the map to make the ice platform

    def __init__(self, ent):
        _Obstacle.__init__(self, ent, self._anim)
        self.anim = 'default'

    def remove(self):
        self.freeze()
        _Obstacle.remove(self)

    def freeze(self):
        lay = self.layer
        X = self.x / 16
        Y = self.y / 16
        for y in range(3):
            for x in range(3):
                ika.Map.SetTile(x + X, y + Y, lay, self._frozenTiles[y][x])
                ika.Map.SetObs(x + X, y + Y, lay, False)

        setattr(savedata, self.flagName, 'True')

class Boulder(_Obstacle):
    def __init__(self, *args):
        self.isTouching = False
        _Obstacle.__init__(self, *args)

    def update(self):
        t = self.touches(system.engine.player)
        if t and not self.isTouching:
            self.isTouching = True

            # find a stick of TNT
            tnt = [k for k in savedata.__dict__.keys()
                if k.startswith('dynamite')
                and savedata.__dict__[k] == 'True']

            if tnt:
                # TODO: explode animation here
                setattr(savedata, tnt[0], 'False')
                setattr(savedata, self.flagName, 'True')
                system.engine.player.stats.tnt-=1
                
                e = ika.Entity(self.x-8, self.y, self.ent.layer+1, 'explosion.ika-sprite')
                system.engine.addEntity(Explosion(e))
                
                system.engine.destroyEntity(self)
                #system.engine.addCaptions(Caption('Blew the rock apart!'))
                automap.map.SetCollected('Boulder')

        else:
            self.isTouching = False

class Explosion(Entity):
    _anim = {
    'default': ((
        ((0, 300),),
        ((1, 300),),
        ((2, 300),),
        ((3, 300),),
        ((4, 300),),
        ((5, 300),),
                
        ),
        False
    )
    }

    
    def __init__(self, ent):
        Entity.__init__(self, ent, self._anim)
        self.anim = 'default'
        self.invincible = True
        self.state = self.boomState()
        self.duration=42
        self.timer=0
        sound.explode.Play()
        
    def boomState(self):   
        while self.timer<self.duration:
            frame=int(self.timer/(self.duration/6))        
            self.ent.specframe=frame       
            self.timer+=1
            yield None
        self.die()
        yield None
