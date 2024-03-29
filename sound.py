
import ika
from thing import Thing
import system


class NullSound(object):
    def __init__(self):
        self.position = 0
        self.volume = 1.0

    def Play(self):
        pass

    def Pause(self):
        pass

class RepeatableSound(object):
    def __init__(self, fname):
        self.fname = fname
        self.sounds = [ika.Sound(fname)]
        self.sounds[0].loop = False

    def Play(self):
        for s in self.sounds:
            if s.position == 0:
                s.Play()
                return

        s = ika.Sound(self.fname)
        s.loop = False
        s.Play()
        self.sounds.append(s)

    def StopAllSounds(self):
        for s in self.sounds:
            s.volume=0 #hack!


# effects:

slash1, slash2, slash3 = [
    RepeatableSound('sfx/swing%i.wav' % i) for i in range(1,4)
    ]
playerHurt = NullSound()

dodge = RepeatableSound('sfx/dodge.ogg')

achievement = RepeatableSound('sfx/LevelUp.wav')

menuClick = RepeatableSound('sfx/MenuClick.wav')
menuBuzz = RepeatableSound('sfx/MenuBuzz.wav')

hearthRend = RepeatableSound('sfx/HearthRend.wav')
crushingGale = RepeatableSound('sfx/CrushingGale.wav')
healingRain = RepeatableSound('sfx/HealingRain.wav')
#boltStorm = RepeatableSound('sfx/bolt2.wav')
boltStorm = RepeatableSound('sfx/slash3.wav')

monsterHit = RepeatableSound('sfx/MonsterHit.wav')

anklebiterStrike = ika.Sound('sfx/AnklebiterStrike.wav')
anklebiterHurt = NullSound() # ika.Sound('sfx/AnklebiterHurt.wav')
anklebiterDie = RepeatableSound('sfx/AnklebiterDie.wav')

beam = RepeatableSound('sfx/beam.wav')
serpentRoar = RepeatableSound('sfx/serpentroar.wav')
serpentDie = RepeatableSound('sfx/serpentdie.wav')

yetiStrike = [NullSound(), NullSound()]
yetiHurt = [[ika.Sound('sfx/YetiHurt%i.wav' % i) for i in range(1,4)],
            [ika.Sound('sfx/SoulReaverHurt%i.wav' % i) for i in range(1,4)]]
yetiDie = [ika.Sound('sfx/YetiDie.wav'), ika.Sound('sfx/SoulReaverDie.wav')]

razorManeStrike = RepeatableSound('sfx/RazormaneStrike.wav')
razorManeHurt = RepeatableSound('sfx/RazormaneHurt.wav')
razorManeDie = RepeatableSound('sfx/RazormaneDie.wav')

step = RepeatableSound('sfx/step.wav')
explode = RepeatableSound('sfx/explode-5.wav')

# other effects?

# music:
# all music.  Never ever let go. (because I'm lazy)
music = {}

music['music/silence'] = NullSound()

class Crossfader(Thing):
    def __init__(self):
        self.oldMusic = []
        self._music = None
        self.inc = 0.01

    def _setMusic(self, value):
        assert value is not None
        self._music = value

    music = property(lambda self: self._music, _setMusic)

    def reset(self, newMusic):
        if newMusic is self.music:
            return

        if newMusic in self.oldMusic:
            self.oldMusic.remove(newMusic)

        if self.music is not None:
            if self.music not in self.oldMusic:
                self.oldMusic.append(self.music)
            self.music = newMusic
            self.music.volume = 0.0
            self.music.Play()
        else:
            self.music = newMusic
            self.music.volume = 1.0
            self.music.Play()

    def kill(self):
        if self.music:
            self.music.volume = 0.0
            self.music.Pause()
            self._music = None
            for m in self.oldMusic:
                m.volume = 0
            self.oldMusic = []

    def update(self):
        i = 0
        while i < len(self.oldMusic):
            m = self.oldMusic[i]
            m.volume -= self.inc
            if m.volume <= 0:
                m.Pause()
                self.oldMusic.pop(i)
            else:
                i += 1

        self.music.volume += self.inc

        if not self.oldMusic and self.music.volume >= 1.0:
            return True

    def draw(self):
        pass

fader = Crossfader()

def playMusic(fname):
    if fname in music:
        m = music[fname]
    else:
        m = ika.Sound(fname)
        m.loop = True
        music[fname] = m

    fader.reset(m)
    if fader not in system.engine.things:
        system.engine.things.append(fader)

def killMusic():
    global musicName
    fader.kill()
