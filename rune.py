from entity import Entity
from caption import Caption
import system
import savedata

from controls import displayControls

class _Rune(Entity):
    def __init__(self, ent):
        super(_Rune, self).__init__(ent, None)
        self.invincible = True
        self.name = self.ent.name

        if self.name in savedata.__dict__:
            self.x = -100
            system.engine.destroyEntity(self)

    def apply(self):
        system.engine.player.calcSpells()

    def update(self):
        if self.touches(system.engine.player):
            system.engine.destroyEntity(self)
            if self.element in ['Strength', 'Guard', 'Power']:
                system.engine.addThing(Caption('%s Rune collected!' % self.element, y=160, duration=400))
                if self.element=='Strength':
                    system.engine.player.stats.strengthrunes+=1           
                if self.element=='Power':
                    system.engine.player.stats.powerrunes+=1           
                if self.element=='Guard':
                    system.engine.player.stats.guardrunes+=1           
            else:
                system.engine.addThing(Caption('You got the %s Rune!' % self.element, y=160, duration=400))
            system.engine.addThing(Caption('%s' % self.effect, y=170, duration=400))
            system.engine.addThing(Caption('%s' % self.effect2, y=180, duration=400))
            setattr(savedata, self.name, 'True')
            self.apply()


class WaterRune(_Rune):
    element = property(lambda self: 'Water')
    effect = property(lambda self: 'Healing Rain spell learned. (%s)' % displayControls['heal'])
    effect2 = property(lambda self: 'Can freeze floating ice formations.')

class FireRune(_Rune):
    element = property(lambda self: 'Fire')
    effect = property(lambda self: 'Hearth Rend spell learned. (%s)' % displayControls['rend'])
    effect2 = property(lambda self: 'Can melt ice blocks.')

class WindRune(_Rune):
    element = property(lambda self: 'Wind')
    effect = property(lambda self: 'Crushing Gale spell learned. (%s)' % displayControls['gale'])
    effect2 = property(lambda self: 'Can cross broken bridges.')

class UnityRune(_Rune):
    element = property(lambda self: 'Lightning')
    effect = property(lambda self: 'Bolt Storm spell learned. (%s)' % displayControls['bolt'])     
    effect2 = property(lambda self: 'Can destroy crystal blocks.')    
        
class BindingRune(_Rune):
    element = property(lambda self: 'Binding')
    effect = property(lambda self: 'Magic +2')
    effect2 = property(lambda self: ' ')
    
class StrengthRune(_Rune):
    def apply(self):
        system.engine.player.stats.att += 2

    element = property(lambda self: 'Strength')
    effect = property(lambda self: 'Attack +2')
    effect2 = property(lambda self: ' ')

class GuardRune(_Rune):
    def apply(self):
        system.engine.player.stats.pres += 2        

    element = property(lambda self: 'Guard')
    effect = property(lambda self: 'Defense +2')
    effect2 = property(lambda self: ' ')

class PowerRune(_Rune):
    def apply(self):
        system.engine.player.stats.mag += 2

    element = property(lambda self: 'Power')
    effect = property(lambda self: 'Magic +2')
    effect2 = property(lambda self: ' ')
