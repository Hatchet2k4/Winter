# Stand-in load/save menu code

import ika
import system
from saveload import SaveGame
from automap import automapdata
from xi.menu import Menu, Cancel
from xi.cursor import ImageCursor
import xi.effects

from xi import gui, layout

import controls
from snow import Snow
from caption import Caption


debug = True

class SaveGameFrame(gui.Frame):
    def __init__(self, *args, **kw):
        gui.Frame.__init__(self, *args, **kw)
        self.save = kw.get('save', None)
        self.layout = layout.VerticalBoxLayout()
        self.addChild(self.layout)
        self.update(kw['icons'])
        

    def update(self, icons):
        if self.save:
            stats = self.save.stats
            
            m=''              
            #if debug: m+=self.save.fname
            if self.save.mapName in automapdata:
                m+=automapdata[self.save.mapName][5]
            c = []
            
            if debug: 
                c += [   layout.HorizontalBoxLayout(
                    gui.StaticText(text=self.save.fname[6:])) ]  #using [6:] to remove saves/ from the text
                        
            c += [                        
                layout.HorizontalBoxLayout(
                    gui.StaticText(text=m),
                ),
            
                layout.HorizontalBoxLayout(
                    gui.StaticText(text='HP. %03i/%03i' % (stats.hp, stats.maxhp)),
                    layout.Spacer(width=16),
                    gui.StaticText(text='Lv. %02i' % stats.level)
                ),                                
                layout.FlexGridLayout(5,    
                    icons['att'], gui.StaticText(text='%02i  ' % stats.att),
                    icons['mag'], gui.StaticText(text='%02i  ' % stats.mag),
                    gui.StaticText(text='  Time'),                    
                    icons['pres'], gui.StaticText(text='%02i  ' % stats.pres),
                    icons['tnt'], gui.StaticText(text='% i  ' % stats.tnt),
                    gui.StaticText(text='  '+self.save.time)
                )
            ]
            
            self.layout.setChildren(c)

            self.layout.layout()
            self.autoSize()
            self.width = 140 #hack! Don't want windows autosized..
        else:
            assert False

New = object()

class SaveLoadMenu(object):
    def __init__(self, saves, saving = False):
        self.icons = dict(
            [(s, gui.Picture(img='gfx/ui/icon_%s.png' % s))
                for s in ('att', 'mag', 'pres', 'tnt')]
        )

        self.cursor = ImageCursor('gfx/ui/pointer.png')

        self.saves = saves
        self.saving = saving

        boxes = [SaveGameFrame(save=s, icons=self.icons) for s in saves]
        if saving:
            boxes.append(gui.TextFrame(text='Create New'))
        elif not boxes:
            b = gui.TextFrame(text='No Saves')
            
            boxes.append(b)

        self.layout = layout.VerticalBoxLayout(pad=16, *boxes)
        self.layout.layout()

        self.cursorPos = 0
        self.oldY = 0 # current offset
        self.curY = 0 # offset we should be at
        self.offset=-14
        
        if boxes:
            self.wndHeight = self.layout.children[0].Height + 16
        else:
            self.wndHeight = 0 # What should we do here?

        self.layout.X = 100 # doesn't change

    def draw(self):
        self.layout.Y = (ika.Video.yres - self.wndHeight) / 2 - self.oldY + 16
        self.layout.draw()
        self.cursor.draw(100, ika.Video.yres / 2 + self.offset) # cursor doesn't move, everything else does
        #self.cursor.draw(100, 3) # cursor doesn't move, everything else does

    def update(self):
        assert len(self.layout.children), 'There should be at least one frame in here. (either indicating no saves, or to create a new save.'
        ika.Input.Update()

        if self.curY < self.oldY:
            self.oldY -= 2
        elif self.curY > self.oldY:
            self.oldY += 2
        else:
            if (controls.up() or controls.ui_up() or controls.joy_up()) and self.cursorPos > 0:
                self.cursorPos -= 1
                self.curY = self.cursorPos * self.wndHeight
            elif (controls.down() or controls.ui_down() or controls.joy_down()) and self.cursorPos < len(self.layout.children) - 1:
                self.cursorPos += 1
                self.curY = self.cursorPos * self.wndHeight
            elif controls.attack() or controls.ui_accept() or controls.joy_attack():
                if self.saving and self.cursorPos == len(self.layout.children) -1: #create new
                    return New
                else: 
                    return self.cursorPos
            elif controls.cancel() or controls.ui_cancel() or controls.joy_cancel():
                return Cancel

            return None

def readSaves():
    saves = []
    
    #try:
    #    saves.append(SaveGame('quicksave')) #if a quicksave exists, why not!           
    #except IOError: 
    #    pass #no file here
    
    for i in range(100): #support 100 saves?! :o
        try:
            saves.append(SaveGame('saves/Save %i' % i))            
        except IOError: 
            pass #no file here, skip to the next one
            
    return saves

def loadMenu(fadeOut=True):
    title = gui.TextFrame(text='Load Game')
    title.Position = (12, 12)
    saves = readSaves()    
    m = SaveLoadMenu(saves, saving=False)
    if len(saves)==0:
        m.offset = 6 #hack to position cursor properly when no saves exist
    bg = ika.Image('gfx/mountains.png')
    
    def draw():
        ika.Video.TintBlit(bg, 0,0, ika.RGB(128, 128, 128, 255))
        m.draw()        
        title.draw()

    xi.effects.fadeIn(50, draw=draw)

    i = None
    while i is None:
        i = m.update()        
        draw()
        ika.Video.ShowPage()
                
    if fadeOut:
        xi.effects.fadeOut(50, draw=draw)

    draw()
    if i is Cancel or i >= len(saves):
        return None
    else:
        return saves[i]


def saveMenu():
    title = gui.TextFrame(text='Save Game')
    title.Position = (16, 16)
    saves = readSaves()
    m = SaveLoadMenu(saves, saving=True)        
    if len(saves)==0:
        m.offset = 6 #hack to position cursor properly when no saves exist
    bg = ika.Image('gfx/mountains.png')
    
    def draw():
        #ika.Video.ClearScreen() # fix this
        ika.Video.TintBlit(bg, 0,0, ika.RGB(128, 128, 128, 255)) #fixed it!
        m.draw()
        title.draw()

    xi.effects.fadeIn(50, draw=draw)

    i = None
    while i is None:
        i = m.update()
        draw()
        ika.Video.ShowPage()

    if i is not Cancel:
        s = SaveGame.currentGame()
        if i is New:
            for j in range(100):
                try: 
                    f=file('saves/Save %i' % j, 'rt')                    
                    f.close()
                except IOError, e: #found a slot that doesn't exist. Bad hack!
                    ika.Log(str(e))
                    s.save('saves/Save %i' % j)
                    system.engine.addCaptions(Caption('Game saved.', duration=100))
                    break
        else:        
            filename=saves[i].fname
            s.save(filename)
            system.engine.addCaptions(Caption('Game saved.', duration=100))

    xi.effects.fadeOut(50, draw=draw)
    

