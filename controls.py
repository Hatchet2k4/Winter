'''
Input abstraction and so on.
'''

import ika

from keynames import keyNames
import controls
import xi.controls

from saveload import SaveGame

useGamePad = False

# Name : Control pairs
_allControls = dict()


defaultControls = {
    #default mappable keyboard keys
    'up': 'UP',
    'down': 'DOWN',
    'left': 'LEFT',
    'right': 'RIGHT',
    'attack': 'SPACE',
    'cancel': 'ESCAPE',
    'rend': 'Z',
    'gale': 'X',
    'heal': 'C',
    'bolt': 'B',
    'showmap': 'TAB',
    #default mappable gamepad buttons
    'joy_up': 'joy0axis1-',
    'joy_down': 'joy0axis1+',
    'joy_left': 'joy0axis0-',
    'joy_right': 'joy0axis0+',
    'joy_attack': 'joy0button1',
    'joy_cancel': 'joy0button2',
    'joy_rend': 'joy0button0',
    'joy_gale': 'joy0button3',
    'joy_heal': 'joy0button4',
    'joy_bolt': 'joy0button5',
    'joy_showmap': 'joy0button9',  
    #unremappable ui keys
    'ui_up': 'UP',
    'ui_down': 'DOWN',
    'ui_left': 'LEFT',
    'ui_right': 'RIGHT',
    'ui_accept': 'RETURN',
    'ui_cancel': 'ESCAPE',
    #to be removed/disabled before release
    'savestate': 'F2',
    'loadstate': 'F4',    
    'speedhack': 'Q'
}

displayControls = {
    #default mappable keyboard keys
    'up': 'UP',
    'down': 'DOWN',
    'left': 'LEFT',
    'right': 'RIGHT',
    'attack': 'SPACE',
    'cancel': 'ESCAPE',
    'rend': 'Z',
    'gale': 'X',
    'heal': 'C',
    'bolt': 'B',
    'showmap': 'TAB',
    #default mappable gamepad buttons
    'joy_up': 'None',
    'joy_down': 'None',
    'joy_left': 'None',
    'joy_right': 'None',
    'joy_attack': 'None',
    'joy_cancel': 'None',
    'joy_rend': 'None',
    'joy_gale': 'None',
    'joy_heal': 'None',
    'joy_bolt': 'None',
    'joy_showmap': 'None',  
    #unremappable ui keys
    'ui_up': 'UP',
    'ui_down': 'DOWN',
    'ui_left': 'LEFT',
    'ui_right': 'RIGHT',
    'ui_accept': 'RETURN',
    'ui_cancel': 'ESCAPE',
    #to be removed/disabled before release, unremappable
    'savestate': 'F2',
    'loadstate': 'F4',    
    'speedhack': 'Q'
}

currentConfig = {}

#joystick friendly names
#_friendlyNames = dict()
firstrun = False

def UnpressAllKeys():
    for k in keyNames: 
        ika.Input.keyboard[k].Pressed()

def init():
    # fill up _allControls
    global useGamePad, firstrun
    # Null control
    _allControls['none'] = lambda: False

    # keyboard keys:
    for k in keyNames:
        _allControls[k] = ika.Input.keyboard[k]
    
    if len(ika.Input.joysticks) > 0:
        if not firstrun: 
            ika.Log(str(len(ika.Input.joysticks)) +' gamepad(s) found:')
        
        # joystick:
        for joyIndex, joy in enumerate(ika.Input.joysticks):        
            # axes:                        
            for axisIndex, axis in enumerate(joy.axes):
                _allControls['joy%iaxis%i+' % (joyIndex, axisIndex)] = axis
                if not firstrun: ika.Log('Gamepad: '+str(joyIndex) + '  axisIndex: ' + str(axisIndex))
                #_friendlyNames['joy%ibutton%i' % (joyIndex, axisIndex)] = 'JoyAxis:'+str(axisIndex)
            for axisIndex, axis in enumerate(joy.reverseAxes):
                if not firstrun: ika.Log('Gamepad: '+str(joyIndex) + '  Reverse axisIndex: ' + str(axisIndex))
                _allControls['joy%iaxis%i-' % (joyIndex, axisIndex)] = axis
                #_friendlyNames['joy%ibutton%i' % (joyIndex, axisIndex)] = 'JoyAxis:'+str(axisIndex)

            # buttons:
            for buttonIndex, button in enumerate(joy.buttons):
                if not firstrun: ika.Log('Gamepad: '+str(joyIndex) + '  buttonIndex: ' + str(buttonIndex))
                _allControls['joy%ibutton%i' % (joyIndex, buttonIndex)] = button
                #_friendlyNames['joy%ibutton%i' % (joyIndex, buttonIndex)] = 'Joy:'+str(buttonIndex)
            
            useGamePad = True #got this far - presumably this worked!
            firstrun = True
    #ika.Log(str(_allControls))

    #setConfig(defaultControls)

# returns a dict
def readConfig(f):
    if isinstance(f, str):
        f = file(f, 'rt')

    config = dict()
    for line in f.readlines():
        l = line.split()[:2]
        config[l[0]] = l[1]

    return config

def writeConfig(f, config):
    if isinstance(f, str):
        f = file(f, 'wt')
    for k, v in config.iteritems():
        print >> f, '%s %s' % (k, v)

buttonmapping = {
'0-': 'Stick Left',
'0+': 'Stick Right',
'1-': 'Stick Up',
'1+': 'Stick Down',
'2-': 'Axis 2-',
'2+': 'Axis 2+',
'3-': 'Axis 3-',
'3+': 'Axis 3+',
'4-': 'Axis 4-',
'4+': 'Axis 4+',
'5-': 'Axis 5-',
'5+': 'Axis 5+',
'6-': 'Axis 6-',
'6+': 'Axis 6+',
'7-': 'Axis 7-',
'7+': 'Axis 7+',
'8-': 'Axis 8-',
'8+': 'Axis 8+',
'9-': 'Axis 9-',
'9+': 'Axis 9+',

'0': 'Button 1',
'1': 'Button 2',
'2': 'Button 3',
'3': 'Button 4',
'4': 'Button 5',
'5': 'Button 6',
'6': 'Button 7',
'7': 'Button 8',
'8': 'Button 9',
'9': 'Button 10',
'10': 'Button 11',
'11': 'Button 12',
'13': 'Button 13',
'14': 'Button 14',
'15': 'Button 15',
'16': 'Button 16',
'17': 'Button 17',
'18': 'Button 18',
'19': 'Button 19',
'20': 'Button 20'
}

joybuttonmapping = {
'0-': 'Stick Left',
'0+': 'Stick Right',
'1-': 'Stick Up',
'1+': 'Stick Down',
'0': 'Button X',
'1': 'Button A',
'2': 'Button B',
'3': 'Button Y',
'4': 'Button L1',
'5': 'Button R1',
'6': 'Button L2',
'7': 'Button R2',
'8': 'Button Select',
'9': 'Button Start',
'10': 'Button L3',
'11': 'Button R3'
}


#left joy0axis0-
#right joy0axis0+
#down joy0axis1+
#up joy0axis1-


        
class NullControl(object):        
    def Pressed(self):
        return False
    def Position(self):
        return 0
    def __call__(self):
        return False
        
def setConfig(config=None):
    class PosControl(object):
        def __init__(self, name):
            self.set(name)
        def set(self, name):        
            self.name = name
            self.config = config[name]
            self.pressed=False #hack for later
            try:
                self.c = _allControls[config[name]]       
                if 'joy' in config[name]: #dealing with a gamepad, hack code follows
                    if 'axis' in config[name]: #stick/dpad
                        #hack, assuming directions always align logically. No up=down here! :P
                        ax = config[name][-2:]
                        if ax in buttonmapping:
                            displayControls[name] = buttonmapping[ax]
                        else:
                            ika.Log('Invalid axis: ' + ax)
                            displayControls[name] = ax
                    else: #button
                        if config[name][-2] in '0123456789': #double digit button
                            b = config[name][-2:] #get last two characters
                        else: #single digit button
                            b =  config[name][-1] #get just last character                    
                        
                        if b in buttonmapping:
                            displayControls[name] = buttonmapping[b]
                        else:
                            displayControls[name] = b
                                       
                else: #regular 
                    displayControls[name] = config[name]
            except:
                ika.Log('Unable to set control '+name) 
                displayControls[name] = 'None'
                self.c = NullControl()
                
        def __call__(self):   return self.c.Position() > 0.5
        def __repr__(self):   return '<Winter control %s>' % self.name

    class PressControl(PosControl):
        def __call__(self):
            if 'axis' in self.config: #hack for axis controls mapped to button actions
                if self.c.Position() > 0.5 and not self.pressed:
                    self.pressed=True
                    return True
                elif self.pressed and not self.c.Position() > 0.5:
                    self.pressed=False                    
                return False    
            else:
                return self.c.Pressed()
    
    global currentConfig

    if config is None:
        config = defaultControls
    
    currentConfig = config.copy()
    
    # Directional controls:
    for name in ('up', 'down', 'left', 'right', 'joy_up', 'joy_down', 'joy_right', 'joy_left'):
        globals()[name] = PosControl(name)
    
    #Dedicated UI controls
    for name in ('ui_up', 'ui_down', 'ui_left', 'ui_right'):
        globals()[name] = PosControl(name)
    
    # Buttons
    for name in ('attack', 'cancel', 'rend', 'gale', 'heal',  'bolt', 'showmap'):
        globals()[name] = PressControl(name)
        globals()['joy_'+name] = PressControl('joy_'+name)

    for name in ('ui_accept', 'ui_cancel', 'savestate', 'loadstate', 'speedhack'):
        globals()[name] = PressControl(name)

    # Copy controls over to xi.
    for c in ('up', 'down', 'left', 'right', 'joy_up', 'joy_down', 'joy_left', 'joy_right', 
            'ui_up', 'ui_down', 'ui_left', 'ui_right', 'ui_accept', 'ui_cancel'):
        setattr(xi.controls, c, getattr(controls, c))
    xi.controls.enter = controls.attack
    xi.controls.cancel = controls.cancel
    xi.controls.joy_enter = controls.joy_attack
    xi.controls.joy_cancel = controls.joy_cancel    
    
    #displayControls=config
    #ika.Log(str(config))

    

# global control objects.  These are all set by setConfig
ui_up = ui_down = ui_left = ui_right = ui_accept = ui_cancel = NullControl()

up = down = left = right = NullControl()
attack = cancel = rend = NullControl()
gale = heal = bolt = NullControl()
showmap = NullControl()

joy_up = joy_down = joy_left = joy_right = NullControl()
joy_attack = joy_cancel = joy_rend = NullControl()
joy_gale = joy_heal = joy_bolt = NullControl()
joy_showmap = NullControl()

savestate = loadstate = NullControl()
speedhack= NullControl()

#baaad
allControls=[ui_up,ui_down,ui_left,ui_right,ui_accept,ui_cancel,
up,down,left,right,attack,cancel,rend,gale,heal,bolt,showmap,
joy_up,joy_down,joy_left,joy_right,joy_attack,joy_cancel,joy_rend,joy_gale,joy_heal,joy_bolt,joy_showmap,
savestate,loadstate,speedhack]

configcontrolsDict = {
'up': up,
'down': down,
'left': left,
'right': right,
'attack': attack,
'cancel': cancel,
'showmap': showmap,
'rend': rend,
'gale': gale,
'heal': heal,
'bolt': bolt,
'joy_up': joy_up,
'joy_down': joy_down,
'joy_left': joy_left,
'joy_right': joy_right,
'joy_attack': joy_attack,
'joy_cancel': joy_cancel,
'joy_showmap': joy_showmap,
'joy_rend': joy_rend,
'joy_gale': joy_gale,
'joy_heal': joy_heal,
'joy_bolt': joy_bolt
}

#used for controls menu, order is important
configcontrolsList = [
'up','down','left', 'right',
'attack','cancel','showmap',
'heal','rend','gale','bolt'
]
