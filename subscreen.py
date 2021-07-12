
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
import automap

from saveload import mapnames

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
            txt.append(displayControls['shiver']+' - Bolt Storm')

        return (gui.StaticText(text=txt),)

class AttribWindow(SubScreenWindow):
    def __init__(self):
        SubScreenWindow.__init__(self)
        self.icons = dict(
            [(s, gui.Picture(img='gfx/ui/icon_%s.png' % s))
                for s in ('att', 'mag', 'pres', 'mres', 'tnt')]
        )

    def createLayout(self):
        #layout.HorizontalBoxLayout(
        #            gui.StaticText(text=m),
        #        )
        return layout.FlexGridLayout(cols=2, pad=0)

    def createContents(self):
        stats = system.engine.player.stats
        tnt=0
        for k in savedata.__dict__.keys():
            if k.startswith('dynamite') and savedata.__dict__[k] == 'True':
                tnt+=1
        
        return (
            #gui.StaticText(text='Stats:'),gui.StaticText(text=''),
            self.icons['att'], gui.StaticText(text=' - %02i' % stats.att),
            self.icons['mag'], gui.StaticText(text=' - %02i' % stats.mag),
            self.icons['pres'], gui.StaticText(text=' - %02i' % stats.pres),
            self.icons['tnt'], gui.StaticText(text=' - %i' % tnt)
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
        #self.inv = InvWindow()
        self.timer = TimerWindow()
        

    def update(self):
        self.statWnd.update()
        self.attribWnd.update()
        self.magWnd.update()
        #self.inv.update()
        self.timer.update()
        
        self.statWnd.dockTop().dockLeft()
        self.attribWnd.Position = (self.statWnd.Left, self.statWnd.Bottom + self.statWnd.Border * 2) # eek
        #self.timer.Position = (self.attribWnd.Left, self.attribWnd.Bottom + self.attribWnd.Border * 2)
        self.timer.Position = (self.statWnd.Left, 240-self.timer.height - 8)
        
        
        w = 113
        self.menu.dockRight().dockTop()
        #self.inv.width = w #same width as menu width at present
        #s1elf.inv.dockRight()
        self.magWnd.width = w
        self.magWnd.dockRight()        
        
        #self.inv.Position = (self.inv.Left, self.menu.Bottom + self.menu.Border * 2 )
        #self.magWnd.Position = (self.magWnd.Left, self.inv.Bottom + self.inv.Border * 2)
        self.magWnd.Position = (self.magWnd.Left, self.menu.Bottom + self.menu.Border * 2)
        
        
        

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
        #t.addChild(self.inv, startRect=(ika.Video.xres, self.inv.Top), time=TIME - 5)
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
        #t.addChild(self.inv, endRect=(ika.Video.xres, self.inv.Top), time=TIME - 5)
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
        #self.inv.draw()
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
        scroll = maxscroll = 110
        topx=12
        topy=12
        automap.map.update()
        
        while True:            
            ika.Video.ScaleBlit(self.images[-1], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)
            
            automap.map.draw(topx, topy-scroll)
            
            ika.Video.ShowPage()
            ika.Input.Update()
            
            if controls.cancel() or controls.showmap(): 
                break
            
            if controls.down() and scroll < maxscroll: 
                scroll+=1
            elif controls.up() and scroll > 0: 
                scroll-=1

