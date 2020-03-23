from entity import Entity
from caption import Caption
import system
import savedata

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
            system.engine.addThing(Caption('~1You got the %s Rune!' % self.element))
            setattr(savedata, self.name, 'True')
            self.apply()


class WaterRune(_Rune):
    element = property(lambda self: 'Water')


class FireRune(_Rune):
    element = property(lambda self: 'Fire')


class WindRune(_Rune):
    element = property(lambda self: 'Wind')


class CowardRune(_Rune):
    element = property(lambda self: 'Coward')
        
        
class BindingRune(_Rune):
    element = property(lambda self: 'Binding')


class StrengthRune(_Rune):

    def apply(self):
        system.engine.player.stats.att += 2

    element = property(lambda self: 'Strength')


class GuardRune(_Rune):

    def apply(self):
        system.engine.player.stats.pres += 2
        system.engine.player.stats.mres += 2

    element = property(lambda self: 'Guard')


class PowerRune(_Rune):

    def apply(self):
        system.engine.player.stats.mag += 2

    element = property(lambda self: 'Power')
