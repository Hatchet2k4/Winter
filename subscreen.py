
import ika

from xi.menu import Menu, Cancel
from xi.scrolltext import ScrollableTextFrame
from xi import gui, layout
from xi.transition import Transition
from xi.window import ImageWindow
from xi.cursor import ImageCursor
import effects
import sound
import system
import savedata
from controls import displayControls
from keynames import keyNames
from gameover import EndGameException

import controls
import automap


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
            txt.append('Healing Rain')      
            txt.append('')                  
        if p.rend:            
            txt.append('Hearth Rend')
            txt.append('')        
        if p.gale:            
            txt.append('Crushing Gale')        
            txt.append('')
        if p.bolt:
            txt.append('Bolt Storm')
            txt.append('')
        return (gui.StaticText(text=txt),)

    def draw(self):
        SubScreenWindow.draw(self)
        p = system.engine.player.stats
        
        y=self.Top+22
        w=self.width
        
        if p.heal:
            x=self.Left
            gui.default_font.Print(x, y, displayControls['heal'])
            if (displayControls['joy_heal'] != 'None'):
                x = self.Left+w - gui.default_font.StringWidth(displayControls['joy_heal'])
                gui.default_font.Print(x, y, displayControls['joy_heal'])
        if p.rend:
            x=self.Left
            gui.default_font.Print(x, y+20, displayControls['rend'])    
            if (displayControls['joy_rend'] != 'None'):
                x = self.Left+w - gui.default_font.StringWidth(displayControls['joy_rend'])
                gui.default_font.Print(x, y+20, displayControls['joy_rend'])      
        if p.gale:
            x=self.Left
            gui.default_font.Print(x, y+40, displayControls['gale'])
            if (displayControls['joy_gale'] != 'None'):
                x = self.Left+w - gui.default_font.StringWidth(displayControls['joy_gale'])
                gui.default_font.Print(x, y+40, displayControls['joy_gale'])
        if p.bolt:
            x=self.Left
            gui.default_font.Print(x, y+60, displayControls['bolt'])
            if (displayControls['joy_bolt'] != 'None'):
                x = self.Left+w - gui.default_font.StringWidth(displayControls['joy_bolt'])
                gui.default_font.Print(x, y+60, displayControls['joy_bolt'])
                
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
            self.icons['tnt'], gui.StaticText(text=' - %02i' % tnt)
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
            'Set Controls',
            'Exit to Title')
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

class MapnameWindow(SubScreenWindow):
    def __init__(self):
        SubScreenWindow.__init__(self)

    def createLayout(self):
        return layout.VerticalBoxLayout()

    def createContents(self):
        txt = [automap.automapdata[system.engine.mapName][5]]

        return (gui.StaticText(text=txt),)

###main pause screen class        
class PauseScreen(object):
    def __init__(self):
        assert _initted
        self.statWnd = StatWindow()
        self.attribWnd = AttribWindow()
        self.magWnd = MagicWindow()
        #self.magWnd = ControlsWindow()
        self.menu = MenuWindow()
        #self.inv = InvWindow()
        self.timer = TimerWindow()
        self.mapname = MapnameWindow()
        
        self.allWindows = [self.statWnd, self.attribWnd, self.magWnd, self.menu, self.timer, self.mapname]
        for w in self.allWindows:
            w.setBorder(15)
        

    def update(self):
        self.statWnd.update()
        self.attribWnd.update()
        self.magWnd.update()
        #self.inv.update()
        self.timer.update()
        self.mapname.update()

        self.statWnd.dockTop().dockLeft()
        self.attribWnd.Position = (self.statWnd.Left, self.statWnd.Bottom + self.statWnd.Border * 2) # eek
        #self.timer.Position = (self.attribWnd.Left, self.attribWnd.Bottom + self.attribWnd.Border * 2)
        self.timer.Position = (self.statWnd.Left, 240-self.timer.height - 8 - self.timer.Border/2)
        
        
        w = 113
        self.menu.dockRight().dockTop()
        #self.inv.width = w #same width as menu width at present
        #s1elf.inv.dockRight()
        self.magWnd.width = 130
        self.magWnd.dockRight()        
        
        #self.inv.Position = (self.inv.Left, self.menu.Bottom + self.menu.Border * 2 )
        #self.magWnd.Position = (self.magWnd.Left, self.inv.Bottom + self.inv.Border * 2)
        self.magWnd.Position = (self.magWnd.Left, self.menu.Bottom + self.menu.Border * 2)
        #self.mapname.Position = (dockBottom().dockRight()
        self.mapname.dockRight().dockBottom()
        
        

        self.statWnd.width = 56 #hack! Don't want windows autosized..
        self.attribWnd.width = 56 #hack! Don't want windows autosized..


    def show(self, usebackground=False):
        # assume the backbuffer is already filled
        if not usebackground: 
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
        t.addChild(self.mapname, startRect=(ika.Video.xres, self.mapname.Top), time=TIME - 5)
        for i in range(TIME):
            t.update(1)
            o = i * 128 / TIME # tint intensity for this frame
            f = i * len(self.images) / TIME # blur image to draw

            if not usebackground:
                ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
                ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o), True)
            else:
                ika.Video.ScaleBlit(self.background, 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
                ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)
                
            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

        self.background = self.images[-1]

    def hide(self, usebackground=False):
        TIME = 40
        t = Transition()
        t.addChild(self.statWnd, endRect=(-self.statWnd.Right, self.statWnd.Top), time=TIME - 5)
        t.addChild(self.attribWnd, endRect=(-self.attribWnd.Right, self.attribWnd.Top), time=TIME - 5)
        t.addChild(self.magWnd, endRect=(ika.Video.xres, self.magWnd.Top), time=TIME - 5)
        t.addChild(self.menu, endRect=(ika.Video.xres, self.menu.Top), time=TIME - 5)
        #t.addChild(self.inv, endRect=(ika.Video.xres, self.inv.Top), time=TIME - 5)
        t.addChild(self.timer, endRect=(-self.timer.Right, self.timer.Top), time=TIME - 5)
        t.addChild(self.mapname, endRect=(ika.Video.xres, self.mapname.Top), time=TIME - 5)
        
        for i in range(TIME - 1, -1, -1):
            t.update(1)
            o = i * 255 / TIME # menu opacity for this frame
            f = i * len(self.images) / TIME # blur image to draw
            if not usebackground:
                ika.Video.ScaleBlit(self.images[f], 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
                ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, o / 2), True)
                self.draw(o)
            else:
                ika.Video.ScaleBlit(self.background, 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
                ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0,128), True)
                self.draw(255)
            
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
        self.mapname.draw()
        

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
                    self.setControls,
                    self.exitGame, # Exit game
                ][result]()

        self.hide()

    def toggleDamage(self):
        system.engine.player.stats.damageind = (1, 0)[system.engine.player.stats.damageind]
        self.menu.textCtrl.text.setText(['Resume','Show Damage: ' + ('OFF', 'ON ')[system.engine.player.stats.damageind], 'Set Controls', 'Exit to Title'])

    def setControls(self):
        self.hide(usebackground=True)
        s=ControlsScreen(self.background)
        s.run()
        self.show(usebackground=True)        
           
    def exitGame(self):
        # TODO: shiny fade out
        
        
        raise EndGameException

class ExitWindow(Menu):
    def __init__(self):
        Menu.__init__(self, textctrl=ScrollableTextFrame())
        self.addText(
            'Yes',  'No')
        self.autoSize()
        self.Border = self.textCtrl.wnd.iLeft.width

_initted = False

def init():
    global _initted
    _initted = True
    gui.init(
        font=ika.Font('system.fnt'),
        wnd=Window('gfx/ui/win_%s.png'),
        csr=ImageCursor('gfx/ui/pointer.png', hotspot=(14, 6))
        )

"""
class MenuWindow(Menu):
    def __init__(self):
        Menu.__init__(self, textctrl=ScrollableTextFrame())
        self.addText(
            'Resume',
            #'Controls',
            #'Load Game',
            'Show Damage: ' + ('OFF', 'ON ')[system.engine.player.stats.damageind],
            'Set Controls',
            'Exit')
        self.autoSize()
        self.Border = self.textCtrl.wnd.iLeft.width
"""
#controls submenu
class ControlsWindow(Menu):
    def __init__(self):
        Menu.__init__(self, textctrl=ScrollableTextFrame())
        #self.select = -1        
        self.refreshContents()        
        self.maxwidth = 0

    #def createLayout(self):
    #    return layout.VerticalBoxLayout()

    #def update(self):
    #    return None

    def refreshContents(self):     

        self.linewidth = gui.default_font.StringWidth('Restore Defaults') #assume this is widest line
        
        txt = []        
        txt.append('Up                                    ') #hack to autosize total window because lazy
        txt.append('Down')
        txt.append('Left')
        txt.append('Right')
        txt.append('Attack/Accept')
        txt.append('Cancel/Menu')
        txt.append('Open Map')     

                
        p = system.engine.player.stats               
        if p.heal:           
            txt.append('Healing Rain')
        else:
            txt.append('Spell 1')                    
        if p.rend:
            txt.append('Hearth Rend')
        else:
            txt.append('Spell 2')
        if p.gale:
            txt.append('Crushing Gale')        
        else:
            txt.append('Spell 3')
        if p.bolt:
            txt.append('Bolt Storm')
        else:
            txt.append('Spell 4')
            
        
        txt.append("Restore Default Controls")        
        txt.append("Restore Saved Controls")        
        txt.append("Save Controls")
        txt.append("Exit")        

        self.lastcontrol = len(txt)-5
        self.default = len(txt)-4
        self.restore = len(txt)-3
        self.save = len(txt)-2
        self.exit = len(txt)-1
             
        self.addText(*txt)
        self.autoSize()
        

class Header(gui.TextFrame):
    def __init__(self, x = 0, y = 0, width = 0, height = 0, *args, **kwargs):
        gui.TextFrame.__init__(self, x, y, width, height, *args, **kwargs)

    def draw(self, x1, x2):
        gui.TextFrame.draw(self)
        gui.default_font.Print(x1, self.Top+2, 'Keyboard')
        gui.default_font.Print(x2, self.Top+2, 'Gamepad')

class ControlsScreen(object):
    def __init__(self, background):
        assert _initted
        self.control_menu = ControlsWindow()
        self.control_menu.update()
        self.control_menu.autoSize()
        self.control_menu.Position = (160-self.control_menu.Width/2-8, 48)
        self.background = background
        self.yellowfont = ika.Font('system_yellow.fnt')
        self.greyfont = ika.Font('system_grey.fnt')
        
        self.header = Header(text='Control')
        self.header.setSize( (self.control_menu.Width-16, self.header.Height) )
        self.header.Position=(self.control_menu.Left+16, self.control_menu.Top - self.header.Height*3)
        self.text = ''
        
    def show(self):
        TIME = 40
        self.update()
        t = Transition()
        t.addChild(self.control_menu, startRect=(self.control_menu.Left, 240+self.control_menu.Top), time=TIME - 5)
        t.addChild(self.header, startRect = (self.header.Left, -40), time = TIME-5)
        for i in range(TIME):
            t.update(1)
            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

    def hide(self):
        TIME = 40
        self.update()
        t = Transition()
        t.addChild(self.control_menu, endRect=(self.control_menu.Left, 240+self.control_menu.Top), time=TIME - 5)
        t.addChild(self.header, endRect = (self.header.Left, -40), time = TIME-5)
        for i in range(TIME):
            t.update(1)                
            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()
            

    def draw(self, selected = -1):     
        ika.Video.ScaleBlit(self.background, 0, 0, ika.Video.xres, ika.Video.yres, ika.Opaque)
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, 128), True)         
        self.control_menu.draw()        
     

        h = gui.default_font.height
        x = self.control_menu.Left+self.control_menu.linewidth + 20
        offset=75
        self.header.draw(x, x+offset)
        
        for i, name in enumerate( ['up', 'down', 'left', 'right', 'attack', 'cancel', 'showmap', 'heal', 'rend', 'gale', 'bolt']):           
            y = self.control_menu.Top + h*i
            if i != selected: 
                if displayControls[name] == 'None':
                    self.greyfont.Print(x, y, displayControls[name])
                else:
                    gui.default_font.Print(x, y, displayControls[name])
                if displayControls['joy_'+name] == 'None':
                    self.greyfont.Print(x+offset, y, displayControls['joy_'+name])
                else: #hack hack
                    gui.default_font.Print(x+offset, y, displayControls['joy_'+name])
            else:
                self.yellowfont.Print(x, y, displayControls[name])
                self.yellowfont.Print(x+offset, y, displayControls['joy_'+name])
        
            
        w = gui.default_font.StringWidth(self.text) / 2
        gui.default_font.Print(160-w, 220, self.text)

    def update(self):
        self.control_menu.update()
                        
    def run(self):
        self.show()
        selectmode = 0 #nothing selected
        done = False
        selected = -1 
        
        ika.Input.Unpress()
        
        while not done:                              
            self.draw(selected)                                    
            ika.Video.ShowPage()
            ika.Input.Update()
            
            if selectmode == 0:
                if controls.cancel() or controls.ui_cancel(): 
                    done = True
                    
                result = self.control_menu.update()
                                
                if isinstance(result, int):
                    if result >= 0 and result <= self.control_menu.lastcontrol:
                        selectmode=1 #now poll for input!
                        selected = result #-3 because top options
                        controls.UnpressAllKeys()                  
                        self.text = 'Press Escape to Cancel, Backspace to clear.'                        
                    elif result == self.control_menu.default:
                        controls.setConfig(controls.defaultControls)
                        self.text = 'Default Controls Loaded'
                    elif result == self.control_menu.save:
                        c=controls.currentConfig
                        try:
                            controls.writeConfig('controls.cfg', c)
                            self.text = 'Controls Saved'
                        except:
                            self.text = 'Error saving controls.cfg' 
                    elif result == self.control_menu.restore:
                         try:
                            c = controls.readConfig('controls.cfg')
                            controls.setConfig(c)
                            self.text = 'Controls Loaded'
                         except:                            
                            self.text = 'Error loading controls.cfg' 
                    elif result == self.control_menu.exit:
                        done = True

            else: #polling for input now
                polling = True
                controls.UnpressAllKeys()
                joyconfirm=controls.joy_attack()
                unpress = False
                while polling:
                    self.draw(selected)                                    
                    ika.Video.ShowPage()
                    ika.Input.Update()
  
                    for k in keyNames: #check keyboard 
                        key = ika.Input.keyboard[k]
                        if key.Pressed(): #key pressed!
                            if k == 'ESCAPE': #skip escape         
                                polling = False
                                self.text=''
                                break  
                            elif k == 'BACKSPACE':                                    
                                controls.currentConfig[ controls.configcontrolsList[selected] ] = 'None'
                                controls.currentConfig[ 'joy_'+controls.configcontrolsList[selected] ] = 'None'
                                controls.setConfig(controls.currentConfig)
                                self.text = 'Control cleared'
                                polling=False
                                break
                            else:
                                badkey=False
                                for c in controls.configcontrolsDict.keys():
                                    d = controls.currentConfig[c]
                                    if k == d:
                                        sound.menuBuzz.Play()
                                        self.text = 'Key ' + k + ' already assigned.'
                                        badkey=True
                                        polling=False
                                        break
                                if not badkey:                                    
                                    controls.currentConfig[ controls.configcontrolsList[selected] ] = k
                                    controls.setConfig(controls.currentConfig)
                                    polling = False
                                    self.text = ''                                                                            
                                break    
                     
                    if joyconfirm and not controls.joy_attack():
                        joyconfirm = False
                    
                    if unpress: #hack hack hack
                        repress = False
                        for joyIndex in range(len(ika.Input.joysticks)):
                            for axisIndex in range(len(ika.Input.joysticks[joyIndex].axes)):
                                if ika.Input.joysticks[joyIndex].axes[axisIndex].Position() > 0.5:
                                    repress = True 
                            for axisIndex in range(len(ika.Input.joysticks[joyIndex].reverseAxes)):
                                if ika.Input.joysticks[joyIndex].reverseAxes[axisIndex].Position() > 0.5: 
                                    repress = True 
                        unpress = repress
                    
                    
                    if len(ika.Input.joysticks) > 0 and not joyconfirm: #check gamepad only if gamepad confirm button was unpressed
                        badkey=False
                        for joyIndex in range(len(ika.Input.joysticks)):
                            for axisIndex in range(len(ika.Input.joysticks[joyIndex].axes)):
                                if ika.Input.joysticks[joyIndex].axes[axisIndex].Position() > 0.5 and not unpress:
                                    unpress = True
                                    ax = 'joy%iaxis%i+' % (joyIndex, axisIndex)
                                    for c in controls.configcontrolsDict.keys():
                                        d = controls.currentConfig[c]
                                        if ax==d:
                                            sound.menuBuzz.Play()
                                            self.text = controls.buttonmapping[str(axisIndex)+'+']  +' already assigned.'
                                            badkey=True
                                            break                                            
                                    if not badkey:                                               
                                        controls.currentConfig[ 'joy_'+controls.configcontrolsList[selected] ] = ax       
                                        controls.setConfig(controls.currentConfig)
                                        polling = False    
                                        self.text = ''                                    
                                    break
                            for axisIndex in range(len(ika.Input.joysticks[joyIndex].reverseAxes)):
                                if ika.Input.joysticks[joyIndex].reverseAxes[axisIndex].Position() > 0.5 and not unpress:
                                    unpress = True
                                    ax = 'joy%iaxis%i-' % (joyIndex, axisIndex)
                                    for c in controls.configcontrolsDict.keys():
                                        d = controls.currentConfig[c]
                                        if ax==d:
                                            sound.menuBuzz.Play()
                                            self.text = controls.buttonmapping[str(axisIndex)+'-'] + ' already assigned.'
                                            badkey=True
                                            break   
                                    if not badkey:   
                                        controls.currentConfig[ 'joy_'+ controls.configcontrolsList[selected] ] = ax       
                                        controls.setConfig(controls.currentConfig)
                                        polling = False 
                                        self.text = ''                                    
                                    break                                                                        
                            for buttonIndex in range(len(ika.Input.joysticks[joyIndex].buttons)):
                                if ika.Input.joysticks[joyIndex].buttons[buttonIndex].Pressed():
                                    btn = 'joy%ibutton%i' % (joyIndex, buttonIndex)
                                    for c in controls.configcontrolsDict.keys():
                                        d = controls.currentConfig[c]
                                        if btn==d:
                                            sound.menuBuzz.Play()
                                            self.text = controls.buttonmapping[str(buttonIndex)] + ' already assigned.'
                                            badkey=True
                                            break                                    
                                    if not badkey:                                       
                                        controls.currentConfig[ 'joy_'+ controls.configcontrolsList[selected] ] = btn       
                                        controls.setConfig(controls.currentConfig)
                                        polling = False    
                                        self.text = ''                                                                        
                                    break
                controls.UnpressAllKeys()
                selectmode = 0
                selected = -1
                self.control_menu.unpress=True
                

        self.hide()    





