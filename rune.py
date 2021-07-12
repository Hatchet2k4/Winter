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
            system.engine.addThing(Caption('You got the %s Rune!' % self.element, y=160))
            system.engine.addThing(Caption('%s' % self.effect, y=170))
            setattr(savedata, self.name, 'True')
            self.apply()


class WaterRune(_Rune):
    element = property(lambda self: 'Water')
    effect = property(lambda self: 'Healing Rain spell learned. (%s)' % displayControls['heal'])

class FireRune(_Rune):
    element = property(lambda self: 'Fire')
    effect = property(lambda self: 'Hearth Rend spell learned. (%s)' % displayControls['rend'])

class WindRune(_Rune):
    element = property(lambda self: 'Wind')
    effect = property(lambda self: 'Crushing Gale spell learned. (%s)' % displayControls['gale'])

class CowardRune(_Rune):
    element = property(lambda self: 'Lightning')
    effect = property(lambda self: 'Bolt Storm spell learned. (%s)' % displayControls['shiver'])        
        
class BindingRune(_Rune):
    element = property(lambda self: 'Binding')
    effect = property(lambda self: 'Magic +2')

class StrengthRune(_Rune):

    def apply(self):
        system.engine.player.stats.att += 2

    element = property(lambda self: 'Strength')
    effect = property(lambda self: 'Attack +2')

class GuardRune(_Rune):

    def apply(self):
        system.engine.player.stats.pres += 2
        #system.engine.player.stats.mres += 2

    element = property(lambda self: 'Guard')
    effect = property(lambda self: 'Defense +2')

class PowerRune(_Rune):

    def apply(self):
        system.engine.player.stats.mag += 2

    element = property(lambda self: 'Power')
    effect = property(lambda self: 'Magic +2')
