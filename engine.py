import ika

from serpens.StatelessProxy import StatelessProxy

import effects

import dir

from player import Player

from anklebiter import AnkleBiter
from carnivore import Carnivore
from devourer import Devourer
from razormane import RazorMane
from dragonpup import DragonPup
from hellhound import HellHound
from yeti import Yeti
from gorilla import Gorilla
from soulreaver import SoulReaver

from dynamite import Dynamite
from savepoint import SavePoint
from obstacle import IceWall, Gap, IceChunks, Boulder, Crystal
from rune import WaterRune, FireRune, WindRune, UnityRune, StrengthRune, PowerRune, GuardRune

from field import Field
from hud import HPBar, MPBar, EXPBar
from caption import Caption
from camera import Camera
from gameover import EndGameException, GameOverException, LoadStateException

import subscreen
import saveload
import saveloadmenu
from saveload import SaveGame

import controls
import cabin
import sound
import automap


MAX_SKIP_COUNT = 10
START_MAP = 'map01.ika-map'
START_POS = (34 * 16, 23  * 16)

spawnMap = {
    # match each sprite name up with the associated class
    'anklebiter.ika-sprite': AnkleBiter,
    'carnivore.ika-sprite': Carnivore,
    'devourer.ika-sprite': Devourer,
    'razormane.ika-sprite': RazorMane,
    'dragonpup.ika-sprite': DragonPup,
    'hellhound.ika-sprite': HellHound,
    'yeti.ika-sprite': Yeti,
    'gorilla.ika-sprite': Gorilla,
    'soulreaver.ika-sprite': SoulReaver,

    'dynamite.ika-sprite': Dynamite,
    'waterrune.ika-sprite': WaterRune,
    'firerune.ika-sprite': FireRune,
    'windrune.ika-sprite': WindRune,
    'unityrune.ika-sprite': UnityRune,
    'strengthrune.ika-sprite': StrengthRune,
    'powerrune.ika-sprite': PowerRune,
    'guardrune.ika-sprite': GuardRune,

    'savepoint.ika-sprite': SavePoint,

    'icecave.ika-sprite': IceWall,
    'ice.ika-sprite': IceWall,
    'crystal.ika-sprite': Crystal,
    'icechunks.ika-sprite': IceChunks,
    'boulder.ika-sprite': Boulder,
    'vgap.ika-sprite': Gap,
    'hgap.ika-sprite': Gap,
}

class Engine(object):
    '''Core engine thingie.  bleh.'''

    def __init__(self):
        self.entities = []
        self.killList = []
        self.things = []
        self.mapThings = [] # same as self.things, but is cleared every mapSwitch
        self.fields = []
        self.framerate = 100
        # ika Entity : Entity
        self.entFromEnt = {}

        self.player = None
        self.background = None

        # framerate regulating stuff:
        self.ticksPerFrame = 100.0 / self.framerate
        self.nextFrameTime = 0

        self.font = ika.Font('system.fnt')
        self.mapName = ''
        
        #for game clock
        self.resetTime()
        self.mapscreen = automap.MapScreen()
    
    def SetFrameRate(self, rate):
        self.framerate = rate
        self.ticksPerFrame = 100.0 / self.framerate
    
    def resetTime(self, s=0,m=0,h=0):
        self.seconds = s
        self.minutes = m
        self.hours = h
        self.ticks = 0
        self.time = ''

    def init(self, saveData = None):

        # clean everything
        self.killList = self.entities[:]
        self.clearKillQueue()
        self.things = []
        self.mapThings = []
        self.fields = []
        

        # ika Entity : Entity
        self.entFromEnt = {}

        if saveData:
            # evil
            self.resetTime(saveData.seconds,saveData.minutes,saveData.hours)
            self.mapSwitch(saveData.mapName, None, fade=False)
        else:
            self.resetTime()
            self.mapSwitch(START_MAP, None, fade=False)

        if not self.player:
            self.player = Player()
        self.addEntity(self.player)

        if saveData:
            self.player.x, self.player.y, self.player.layer = saveData.pos
            saveData.setCurrent() # set stats, flags
        else:
            self.player.x, self.player.y = START_POS
            lay = ika.Map.GetMetaData()['entityLayer']
            self.player.layer = ika.Map.FindLayerByName(lay)

        self.things.append(HPBar())
        self.things.append(MPBar())
        self.things.append(EXPBar())

        self.camera = Camera()
        self.camera.center()
        self.things.append(self.camera)
        
        #self.saveallmaps()
        

    def beginNewGame(self):
        saveload.SaveGame.clearSaveFlags()
        #cabin.scene('intro')

        self.mapSwitch(START_MAP, START_POS, fade = False)
        lay = ika.Map.GetMetaData()['entityLayer']

        self.init()

        # insanely inefficient:
        bleh = effects.createBlurImages()
        self.draw()
        effects.blurFade(50, bleh, effects.createBlurImages())
        automap.map.update()
        self.run()

    def loadGame(self, s=None):
        import saveloadmenu
        if not s:
            result = saveloadmenu.loadMenu(fadeOut=False)
        else:
            result = s
            
        if result:
            bleh = effects.createBlurImages()
            saveload.SaveGame.clearSaveFlags()
            self.mapSwitch(result.mapName, result.pos,  fade=False)
            self.init(result)
            self.draw()
            effects.blurFade(50, bleh, effects.createBlurImages())
            self.run()

    def mapSwitch(self, mapName, dest = None, fade = True):
        if fade:
            self.draw()
            startImages = effects.createBlurImages()

        self.mapName = mapName

        # all maps load from the maps/ subdirectory
        mapName = 'maps/' + mapName
        self.background = None
        self.mapThings = []
        self.fields = []
        ika.Map.entities.clear()

        # drop the extension, convert slashes to dots, and prepend the maps package
        # ie 'blah/map42.ika-map' becomes 'maps.blah.map42'
        moduleName = mapName[:mapName.rfind('.')].replace('/', '.')
        mapModule = __import__(moduleName, globals(), locals(), [''])
        ika.Map.Switch(mapName)
        metaData = ika.Map.GetMetaData()
        

        self.readZones(mapModule)
        self.readEnts(mapModule)
        if self.player:
            self.player.state = self.player.defaultState()
        if dest and self.player:
            if len(dest) == 2:
                self.player.x, self.player.y = dest
                lay = metaData['entityLayer']
                self.player.layer = ika.Map.FindLayerByName(lay)
            elif len(dest) == 3:
                self.player.x, self.player.y, self.player.layer = dest
            else:
                assert False

            self.camera.center()
        
        if self.player:
            automap.map.update()

        if 'music' in metaData:                
            sound.playMusic('music/' + metaData['music'])                

        if fade:
            self.draw()
            endImages = effects.createBlurImages()
            effects.blurFade(50, startImages, endImages)

        self.synchTime()

    def warp(self, dest, fade = True):
        if fade:
            self.draw()
            img = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)

        self.player.direction = dir.DOWN
        self.player.state = self.player.defaultState()
        self.player.anim = 'stand'
        self.player.animate()

        self.player.x, self.player.y = dest
        self.camera.center()

        self.draw()
        if fade:
            effects.crossFade(50, startImage = img)
        self.synchTime()

    def run(self):
        try:
            skipCount = 0
            self.nextFrameTime = ika.GetTime() + self.ticksPerFrame
            while True:
                t = ika.GetTime()

                # if we're ahead, delay
                if t < self.nextFrameTime:
                    ika.Delay(int(self.nextFrameTime - t))

                if controls.cancel() or controls.ui_cancel() or controls.joy_cancel():
                    self.pause()

                if controls.savestate():
                    self.SaveState()
                
                if controls.loadstate():
                    self.LoadState()
                
                if controls.showmap():
                    self.ShowMap()

                if controls.speedhack():
                    if self.framerate == 100:
                        self.SetFrameRate(200)                        
                    else: 
                        self.SetFrameRate(100)
                        

                # Do some thinking
                self.tick()

                # if we're behind, and can, skip the frame.  else draw
                if t > self.nextFrameTime and skipCount < MAX_SKIP_COUNT:
                    skipCount += 1
                else:
                    skipCount = 0
                    self.draw()
                    ika.Video.ShowPage()
                    ika.Input.Update()

                self.nextFrameTime += self.ticksPerFrame

        except GameOverException:
            self.gameOver()
            self.killList = self.entities[:]
            self.clearKillQueue()
        
        except LoadStateException, l:
            self.killList = self.entities[:]
            self.clearKillQueue()
            saveload.quicksave=l.s #assign quicksave to be loaded, to be interpreted back in system.py

        except EndGameException: #must be last
            self.killList = self.entities[:]
            self.clearKillQueue()            

    def draw(self):
        if self.background:
            ika.Video.ScaleBlit(self.background, 0, 0, ika.Video.xres, ika.Video.yres)
            ika.Map.Render(*range(ika.Map.layercount))
        else:
            ika.Map.Render()

        for t in self.things:
            t.draw()
        for t in self.mapThings:
            t.draw()

    def tick(self):
        # We let ika do most of the work concerning entity movement.
        # (in particular, collision detection)
        ika.ProcessEntities()

        # update entities
        for ent in self.entities:
            ent.update()
        self.clearKillQueue()

        # check fields
        for f in self.fields:
            if f.test(self.player):
                f.fire()
                break
        
        self.updateTime()

        # update Things.
        # for each thing in each thing list, we update.
        # If the result is true, we delete the thing, else
        # move on.
        for t in (self.things, self.mapThings):
            i = 0
            while i < len(t):
                result = t[i].update()

                if result:  t.pop(i)
                else:       i += 1

    def setPlayer(self, player):
        assert self.player is None

    def addEntity(self, ent):
        assert ent not in self.entities

        self.entities.append(ent)
        self.entFromEnt[ent.ent] = ent

    def destroyEntity(self, ent):
        ent.x = ent.y = -1000
        ent.stop()
        self.killList.append(ent)

    def addField(self, field):
        assert field not in self.fields
        self.fields.append(field)

    def destroyField(self, field):
        self.fields.remove(field)

    def addThing(self, thing):
        self.things.append(thing)

    def destroyThing(self, thing):
        self.things.remove(thing)

    def readZones(self, mapModule):
        '''Read all the zones on the map, and create fields.'''
        self.fields = []

        for i in range(ika.Map.layercount):
            zones = ika.Map.GetZones(i)
            for (x, y, w, h, script) in zones:
                self.addField(Field((x,y,w,h), i, mapModule.__dict__[script]))

    def readEnts(self, mapModule):
        '''Grabs all entities from the map, and adds them to the engine.'''

        # making a gamble here: assuming all entities except the player are tied to the map
        if self.player:
            self.killList= self.entities[:]            
            
            self.killList.remove(self.player)            
            self.clearKillQueue()

        for ent in ika.Map.entities.itervalues():
            try:
                self.addEntity(spawnMap[ent.sprite](ent))
            except KeyError:
                print 'Unknown entity sprite %s.  Ignoring.' % ent.sprite

    def clearKillQueue(self):
        # it's a bad idea to tweak the entity list in the middle of an iteration,
        # so we queue them up, and nuke them here.
        for ent in self.killList:
            ent.ent.x, ent.ent.y = -100,0
            ent.ent.Stop()
            del self.entFromEnt[ent.ent]
            ika.Map.entities.pop(ent, None)
            ent.destroy()
            self.entities.remove(ent)

        self.killList = []

    def testCollision(self, ent):
        e = ent.ent.DetectCollision()
        return self.entFromEnt.get(e)

    def synchTime(self):
        '''Used to keep the engine from thinking it has to catch up
        after executing an event or something.'''

        self.nextFrameTime = ika.GetTime()

    def gameOver(self):
        c = Caption('G A M E   O V E R', duration=1000000, y=(ika.Video.yres - self.font.height) / 2)
        t = 80
        i = 0
        self.fields = []
        while True:
            i = min(i + 1, t)
            c.update()
            self.tick()
            self.draw()

            # darken the screen, draw the game over message:
            o = i * 255 / t
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o), True)
            c.draw()

            ika.Video.ShowPage()
            ika.Delay(4)

            if i == t and (controls.attack() or controls.joy_attack() or controls.ui_accept() or controls.ui_cancel() or controls.cancel() or controls.joy_cancel()):
                break

    def pause(self):
        self.draw()
        s = subscreen.PauseScreen()
        s.run()

        self.synchTime()
    
    def ShowMap(self):
        self.draw()
        self.mapscreen.run()
        self.synchTime()
        
    def updateTime(self):
        self.ticks+=1
        while self.ticks >= 100:
            self.ticks -= 100
            self.seconds += 1
        while self.seconds >= 60:
            self.seconds -= 60
            self.minutes += 1
        while self.minutes >= 60:
            self.minutes -= 60
            self.hours += 1
        #self.time = '%01d:%02d:%02d' % (self.hours, self.minutes, self.seconds)
        self.time = '%01d:%02d' % (self.hours, self.minutes)
        
    def SaveState(self):        
        s = SaveGame.currentGame()
        s.save('quicksave')
        
    def LoadState(self):       
        try:
            s = SaveGame('quicksave')                        
            raise LoadStateException(s)
        except IOError: #no file here            
            sound.menuBuzz.Play()

       
            #bleh = effects.createBlurImages()
            #saveload.SaveGame.clearSaveFlags()
            #self.mapSwitch(s.mapName, s.pos,  fade=False)
            #self.init(s)
            #self.draw()
            #effects.blurFade(50, bleh, effects.createBlurImages())
            #self.run()            
 


        
    