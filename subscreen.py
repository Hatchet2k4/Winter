
import ika

from xi.menu import Menu, Cancel
from xi.scrolltext import ScrollableTextFrame
from xi import gui, layout
from xi.transition import Transition
from xi.window import ImageWindow
from xi.cursor import ImageCursor
import effects

import system
import savedata
from controls import displayControls

from gameover import EndGameException

import controls
import riptiles

automapdata = { #automap data for all maps because I'm lazy, in (x, y, w, h, layer) notation
'map01.ika-map' : (10, 32, 3, 2, 'snow'),
'map02.ika-map' : (7, 30, 3, 3, 'snow'),
'map03.ika-map' : (2, 30, 5, 2, 'snow'),
'map04.ika-map' : (7, 30, 2, 3, 'snow'),
'map05.ika-map' : (2, 26, 1, 1, 'cave'),
'map06.ika-map' : (8, 18, 3, 3, 'snow'),
#'map07.ika-map' : (7, 30, 3, 3, 'snow'),
'map08.ika-map' : (5, 19, 3, 2, 'snow'),
'map11.ika-map' : (5, 21, 3, 2, 'snow'),
} 

class Window(ImageWindow):
    '''
    Specialized xi window.  The only real differences are that it pulls
    its images from separate image files instead of cutting up a single
    image.
    '''
    def __init__(self, nameTemplate):
        self.iTopleft, self.iTopright, self.iBottomleft, self.iBottomright = [
            ika.Image(nameTemplate % i) for i in
                ('top_left', 'top_right', 'bottom_left', 'bottom_right')]
        self.iLeft, self.iRight, self.iTop, self.iBottom = [
            ika.Image(nameTemplate % i) for i in
                ('left', 'right', 'top', 'bottom')]

        self.iCentre = ika.Image(nameTemplate % 'background')

        self.Blit = ika.Video.ScaleBlit
        self.border = 0

class SubScreenWindow(gui.Frame):
    def __init__(self, *args, **kw):
        gui.Frame.__init__(self, *args, **kw)
        self.layout = self.createLayout()
        self.addChild(self.layout)
        self.Border = self.wnd.iLeft.width

    def createLayout(self):
        return layout.VerticalBoxLayout()

    def update(self):
        stats = system.engine.player.stats

        self.layout.setChildren(self.createContents())
        self.layout.layout()
        self.autoSize()

class StatWindow(SubScreenWindow):
    def createContents(self):
        stats = system.engine.player.stats
        return (
            gui.StaticText(text='Level %02i' % stats.level),
            gui.StaticText(text='Exp'), gui.StaticText(text=' %05i/' % stats.exp),
            gui.StaticText(text=' %05i' % stats.next),
            # expbar thingie goes here
            gui.StaticText(text='HP'), gui.StaticText(text=' %03i/%03i' % (stats.hp, stats.maxhp)),
            # hp bar
            gui.StaticText(text='MP'), gui.StaticText(text=' %03i/%03i' % (stats.mp, stats.maxmp)),
            # mp bar
            
            
            )



class MagicWindow(SubScreenWindow):
    def __init__(self):
        SubScreenWindow.__init__(self)

    def createLayout(self):
        return layout.VerticalBoxLayout()

    def createContents(self):
        txt = ['Magic:']
        p = system.engine.player.stats
        if p.heal:
            txt.append(displayControls['heal']+' - Healing Rain ')
        if p.rend:
            txt.append(displayControls['rend']+' - Hearth Rend ')
        if p.gale:
            txt.append(displayControls['gale']+' - Crushing Gale ')        
        if p.shiver:
            txt.append(displayControls['shiver']+' - Nova')

        return (gui.StaticText(text=txt),)

class AttribWindow(SubScreenWindow):
    def __init__(self):
        SubScreenWindow.__init__(self)
        self.icons = dict(
            [(s, gui.Picture(img='gfx/ui/icon_%s.png' % s))
                for s in ('att', 'mag', 'pres', 'mres')]
        )

    def createLayout(self):
        #layout.HorizontalBoxLayout(
        #            gui.StaticText(text=m),
        #        )
        return layout.FlexGridLayout(cols=2, pad=0)

    def createContents(self):
        stats = system.engine.player.stats
        return (
            #gui.StaticText(text='Stats:'),gui.StaticText(text=''),
            self.icons['att'], gui.StaticText(text=' - %02i' % stats.att),
            self.icons['mag'], gui.StaticText(text=' - %02i' % stats.mag),
            self.icons['pres'], gui.StaticText(text=' - %02i' % stats.pres)
            #self.icons['mres'], gui.StaticText(text=' - %02i' % stats.mres)
            )

class InvWindow(SubScreenWindow):
    def __init__(self):
        SubScreenWindow.__init__(self)
        self.icons = {'tnt': gui.Picture(img='gfx/ui/item_dynamite.png'),
                      'strength': gui.Picture(img='gfx/ui/icon_strength.png'),
                      'def': gui.Picture(img='gfx/ui/icon_pres.png'),
                      'mag': gui.Picture(img='gfx/ui/icon_mag.png'),
                      } 
        self.font = system.engine.font
        
    def createLayout(self):
        return layout.FlexGridLayout(cols=2, pad=2)

    def createContents(self):
        
        #txt = [gui.StaticText(text=''), gui.StaticText(text='Inventory') ]
        txt = [gui.StaticText(text=''), gui.StaticText(text='   Items') ]
        
        tnt = 0
        
        strengthrunes=0
        magicrunes=0
        
        for k in savedata.__dict__.keys():
            if k.startswith('dynamite') and savedata.__dict__[k] == 'True':
                tnt+=1
            if k.startswith('strength') and savedata.__dict__[k] == 'True':
                strengthrunes+=1
        if tnt: 
            txt += [self.icons['tnt'], gui.StaticText(text=' - %i' % tnt) ]
        if strengthrunes:
            txt += [self.icons['strength'], gui.StaticText(text=' - %i' % strengthrunes) ]
        
        #else: 
        #    txt += [gui.StaticText(text=''),gui.StaticText(text='')]


        return tuple(txt)

        
        #def draw(): 
        #    SubScreenWindow.draw(self)
            #ika.Log('drawing inventory?')
        #    self.font.Print(self.Left, self.Top+ 4, 'Inventory:')
        #    self.font.Print(128, 104, 'Inventory:')

class MenuWindow(Menu):
    def __init__(self):
        Menu.__init__(self, textctrl=ScrollableTextFrame())
        self.addText(
            'Resume',
            #'Controls',
            #'Load Game',
            'Show Damage: ' + ('OFF', 'ON ')[system.engine.player.stats.damageind],
            'Exit')
        self.autoSize()
        self.Border = self.textCtrl.wnd.iLeft.width

class TimerWindow(SubScreenWindow):
    def __init__(self):
        SubScreenWindow.__init__(self)

    def createLayout(self):
        return layout.VerticalBoxLayout()

    def createContents(self):
        txt = ['Time: '+system.engine.time]

        return (gui.StaticText(text=txt),)




        
class PauseScreen(object):
    def __init__(self):
        assert _initted
        self.statWnd = StatWindow()
        self.attribWnd = AttribWindow()
        self.magWnd = MagicWindow()
        self.menu = MenuWindow()
        self.inv = InvWindow()
        self.timer = TimerWindow()
        

    def update(self):
        self.statWnd.update()
        self.attribWnd.update()
        self.magWnd.update()
        self.inv.update()
        self.timer.update()
        
        self.statWnd.dockTop().dockLeft()
        self.attribWnd.Position = (self.statWnd.Left, self.statWnd.Bottom + self.statWnd.Border * 2) # eek
        #self.timer.Position = (self.attribWnd.Left, self.attribWnd.Bottom + self.attribWnd.Border * 2)
        self.timer.Position = (self.statWnd.Left, 240-self.timer.height - 8)
        
        
        w = 113
        self.menu.dockRight().dockTop()
        self.inv.width = w #same width as menu width at present
        self.inv.dockRight()
        self.magWnd.width = w
        self.magWnd.dockRight()        
        
        self.inv.Position = (self.inv.Left, self.menu.Bottom + self.menu.Border * 2 )
        self.magWnd.Position = (self.magWnd.Left, self.inv.Bottom + self.inv.Border * 2)
        
        
        

        self.statWnd.width = 56 #hack! Don't want windows autosized..
        self.attribWnd.width = 56 #hack! Don't want windows autosized..


    def show(self):
        # assume the backbuffer is already filled
        self.images = effects.createBlurImages()
        TIME = 40

        self.update()

        t = Transition()
        t.addChild(self.statWnd, startRect=(-self.statWnd.Right, self.statWnd.Top), time=TIME - 5)
        t.addChild(self.attribWnd, startRect=(-self.attribWnd.Right, self.attribWnd.Top), time=TIME - 5)
        t.addChild(self.magWnd, startRect=(ika.Video.xres, self.magWnd.Top), time=TIME - 5)
        t.addChild(self.menu, startRect=(ika.Video.xres, self.menu.Top), time=TIME - 5)
        t.addChild(self.inv, startRect=(ika.Video.xres, self.inv.Top), time=TIME - 5)
        t.addChild(self.timer, startRect=(-self.timer.Right, self.timer.Top), time=TIME - 5)

        for i in range(TIME):
            t.update(1)
            o = i * 128 / TIME # tint intensity for this frame
            f = i * len(self.images) / TIME # blur image to draw

            ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o), True)
            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

        self.background = self.images[-1]

    def hide(self):
        TIME = 40
        t = Transition()
        t.addChild(self.statWnd, endRect=(-self.statWnd.Right, self.statWnd.Top), time=TIME - 5)
        t.addChild(self.attribWnd, endRect=(-self.attribWnd.Right, self.attribWnd.Top), time=TIME - 5)
        t.addChild(self.magWnd, endRect=(ika.Video.xres, self.magWnd.Top), time=TIME - 5)
        t.addChild(self.menu, endRect=(ika.Video.xres, self.menu.Top), time=TIME - 5)
        t.addChild(self.inv, endRect=(ika.Video.xres, self.inv.Top), time=TIME - 5)
        t.addChild(self.timer, endRect=(-self.timer.Right, self.timer.Top), time=TIME - 5)
        
        for i in range(TIME - 1, -1, -1):
            t.update(1)
            o = i * 255 / TIME # menu opacity for this frame
            f = i * len(self.images) / TIME # blur image to draw

            ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o / 2), True)
            self.draw(o)
            ika.Video.ShowPage()
            ika.Input.Update()

    def draw(self, opacity = 255):
        gui.default_window.opacity = opacity
        self.statWnd.draw()
        self.attribWnd.draw()
        self.magWnd.draw()
        self.menu.draw()
        self.inv.draw()
        self.timer.draw()
        

    def run(self):
        self.show()
        while True:
            ika.Video.ScaleBlit(self.images[-1], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)
            self.draw()            
            ika.Video.ShowPage()
            ika.Input.Update()

            result = self.menu.update()
            if result is Cancel or result == 0:
                break
            elif result is not None:
                [
                    'dummy', # should never happen
                    #lambda: None, # Control setup
                    #lambda: None, # Load game
                    self.toggleDamage, # Damange indicator Menu
                    self.exitGame, # Exit game
                ][result]()

        self.hide()

    def toggleDamage(self):
        system.engine.player.stats.damageind = (1, 0)[system.engine.player.stats.damageind]
        self.menu.textCtrl.text.setText(['Resume','Show Damage: ' + ('OFF', 'ON ')[system.engine.player.stats.damageind], 'Exit'])


           
    def exitGame(self):
        # TODO: shiny fade out
        raise EndGameException

_initted = False

def init():
    global _initted
    _initted = True
    gui.init(
        font=ika.Font('system.fnt'),
        wnd=Window('gfx/ui/win_%s.png'),
        csr=ImageCursor('gfx/ui/pointer.png', hotspot=(14, 6))
        )



class MapScreen(object):
    def __init__(self):
        assert _initted
        self.maptiles=riptiles.RipTiles('overworld/maptiles.png', 12, 9)
        self.bg=ika.Image('overworld/mapbg.png')
        
        #self.cavedata:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 31, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 34, 0, 0, 24, 25, 0, 0, 0, 0, 0, 26, 27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 25, 0, 0, 30, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 34, 26, 21, 29, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 28, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 29, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 20, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 21, 27, 0, 0, 0, 24, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 33, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 27, 24, 28, 28, 28, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0, 33, 29, 29, 29, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        self.snowdata=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 6, 10, 7, 6, 7, 2, 0, 0, 0, 0, 0, 0, 6, 10, 10, 7, 0, 0, 0, 0, 0, 0, 12, 5, 13, 12, 13, 0, 0, 0, 0, 0, 8, 9, 15, 11, 11, 16, 0, 0, 0, 0, 0, 0, 15, 11, 16, 15, 16, 0, 0, 0, 0, 0, 6, 7, 8, 9, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 7, 0, 0, 0, 0, 15, 16, 0, 0, 12, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 5, 13, 0, 0, 0, 0, 6, 7, 0, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 6, 10, 7, 0, 15, 16, 6, 7, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 9, 12, 0, 13, 0, 0, 0, 15, 16, 12, 5, 13, 0, 0, 0, 6, 10, 10, 7, 6, 10, 10, 7, 15, 11, 16, 0, 0, 0, 6, 7, 15, 11, 16, 6, 10, 7, 15, 11, 11, 16, 15, 11, 11, 16, 0, 0, 0, 0, 0, 0, 15, 16, 6, 10, 7, 12, 5, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 13, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 16, 0, 0, 0, 0, 18, 0, 0, 0, 0, 6, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 6, 10, 10, 10, 7, 6, 10, 7, 6, 10, 7, 12, 5, 13, 2, 0, 0, 0, 0, 0, 0, 0, 15, 11, 11, 11, 16, 12, 5, 13, 15, 11, 16, 15, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 6, 10, 7, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 11, 16, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.snowicons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    
        self.mapwidth=22
        self.mapheight=35
        self.tilewidth=12
        self.tileheight=9
        
    def update(self):
        pass
        
    def show(self):
        self.images = effects.createBlurImages()
    
    def hide(self):
        pass
    
    def draw(self, opacity = 255):
        pass
    def run(self):
        self.show()            
        while True:            
            ika.Video.ScaleBlit(self.images[-1], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)
            ika.Video.Blit(self.bg, 10,9)
            
            topx=12
            topy=12
            for y in range(self.mapheight):
                for x in range(self.mapwidth):
                    for tset in [self.snowdata, self.snowicons]:
                        tile = tset[y*self.mapwidth+x]
                        if tile: 
                            ika.Video.Blit(self.maptiles[tile-1], topx+(x*self.tilewidth),topy+(y*self.tileheight))
                        
            
            ika.Video.ShowPage()
            ika.Input.Update()
            if controls.cancel() or controls.showmap(): 
                break

