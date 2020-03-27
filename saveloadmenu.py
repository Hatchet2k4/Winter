# Stand-in load/save menu code

import ika
import system
from saveload import SaveGame
from xi.menu import Menu, Cancel
from xi.cursor import ImageCursor
import xi.effects


from xi import gui, layout

import controls
from snow import Snow

mapnames = { #all the maps that have save points
'map02.ika-map' : 'Mount Durinar Base',
'map12.ika-map' : 'Misty Cave', #need to change which map this one's in
'map14.ika-map' : 'Lookout Point',
'map30.ika-map' : 'Serpent Valley',
'map38.ika-map' : 'Northwest Summit',
'map50.ika-map' : 'Northeast Cave'
} 


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
            if self.save.mapName in mapnames:
                m=mapnames[self.save.mapName]
                
            self.layout.setChildren([
                        
                layout.HorizontalBoxLayout(
                    gui.StaticText(text=m),
                ),
            
                layout.HorizontalBoxLayout(
                    gui.StaticText(text='HP%03i/%03i' % (stats.hp, stats.maxhp)),
                    layout.Spacer(width=16),
                    gui.StaticText(text='Lv. %02i' % stats.level)
                ),                                
                layout.FlexGridLayout(4,
                    icons['att'], gui.StaticText(text='%02i  ' % stats.att),
                    icons['mag'], gui.StaticText(text='%02i  ' % stats.mag),
                    icons['pres'], gui.StaticText(text='%02i  ' % stats.pres),
                    icons['mres'], gui.StaticText(text='%02i  ' % stats.mres)
                )
            ])

            self.layout.layout()
            self.autoSize()
            self.width = 128 #hack! Don't want windows autosized..
        else:
            assert False

class SaveLoadMenu(object):
    def __init__(self, saves, saving = False):
        self.icons = dict(
            [(s, gui.Picture(img='gfx/ui/icon_%s.png' % s))
                for s in ('att', 'mag', 'pres', 'mres')]
        )

        self.cursor = ImageCursor('gfx/ui/pointer.png')

        self.saves = saves

        boxes = [SaveGameFrame(save=s, icons=self.icons) for s in saves]
        if saving:
            boxes.append(gui.TextFrame(text='Create New'))
        elif not boxes:
            boxes.append(gui.TextFrame(text='No Saves'))

        self.layout = layout.VerticalBoxLayout(pad=16, *boxes)
        self.layout.layout()

        self.cursorPos = 0
        self.oldY = 0 # current offset
        self.curY = 0 # offset we should be at
        if boxes:
            self.wndHeight = self.layout.children[0].Height + 16
        else:
            self.wndHeight = 0 # What should we do here?

        self.layout.X = 100 # doesn't change

    def draw(self):
        self.layout.Y = (ika.Video.yres - self.wndHeight) / 2 - self.oldY + 16
        self.layout.draw()
        self.cursor.draw(100, ika.Video.yres / 2) # cursor doesn't move, everything else does
        #self.cursor.draw(100, 3) # cursor doesn't move, everything else does

    def update(self):
        assert len(self.layout.children), 'There should be at least one frame in here. (either indicating no saves, or to create a new save.'
        ika.Input.Update()

        if self.curY < self.oldY:
            self.oldY -= 2
        elif self.curY > self.oldY:
            self.oldY += 2
        else:
            if controls.up() and self.cursorPos > 0:
                self.cursorPos -= 1
                self.curY = self.cursorPos * self.wndHeight
            elif controls.down() and self.cursorPos < len(self.layout.children) - 1:
                self.cursorPos += 1
                self.curY = self.cursorPos * self.wndHeight
            elif controls.attack():
                return self.cursorPos
            elif controls.cancel():
                return Cancel

            return None

def readSaves():
    saves = []

    try:
        i = 0
        while True:
            saves.append(SaveGame('save%i' % i))
            i += 1
    except IOError:
        return saves

def loadMenu(fadeOut=True):
    title = gui.TextFrame(text='Load Game')
    title.Position = (12, 12)
    saves = readSaves()
    m = SaveLoadMenu(saves, saving=False)
    
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
        s.save('save%i' % i)

    xi.effects.fadeOut(50, draw=draw)

