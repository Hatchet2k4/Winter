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
    'ui_up': 'UP',
    'ui_down': 'DOWN',
    'ui_left': 'LEFT',
    'ui_right': 'RIGHT',
    'ui_accept': 'RETURN',
    'ui_cancel': 'ESCAPE',
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
    'savestate': 'F2',
    'loadstate': 'F4',
    'showmap': 'TAB',
    'speedhack': 'Q'
}
displayControls = {}

#joystick friendly names
#_friendlyNames = dict()
firstrun = False

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

    setConfig(defaultControls)

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
'11': 'Button R3',
}

#left joy0axis0-
#right joy0axis0+
#down joy0axis1+
#up joy0axis1-

def setConfig(config=None):
    class PosControl(object):
        def __init__(self, name):
            self.name = name
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
                        
                    
                    #    displayControls[name] =#haaack, just grab last character. will break if more than 10 buttons..                
            else: #regular 
                displayControls[name] = config[name]
        def __call__(self):   return self.c.Position() > 0.5
        def __repr__(self):   return '<Winter control %s>' % self.name

    class PressControl(PosControl):
        def __call__(self):
            return self.c.Pressed()

    if config is None:
        config = defaultControls
    # Directional controls:
    for name in ('up', 'down', 'left', 'right'):
        globals()[name] = PosControl(name)
    
    #Dedicated UI controls
    for name in ('ui_up', 'ui_down', 'ui_left', 'ui_right'):
        globals()[name] = PosControl(name)

    # Buttons
    for name in ('attack', 'cancel', 'ui_accept', 'ui_cancel', 
                 'rend', 'gale', 'heal',  'bolt', 
                 'savestate', 'loadstate', 'showmap', 'speedhack'):
        globals()[name] = PressControl(name)
    

    # Copy controls over to xi.
    for c in ('up', 'down', 'left', 'right', 'ui_up', 'ui_down', 'ui_left', 'ui_right', 'ui_accept', 'ui_cancel'):
        setattr(xi.controls, c, getattr(controls, c))
    xi.controls.enter = controls.attack
    xi.controls.cancel = controls.cancel
    
    #displayControls=config
    #ika.Log(str(config))

    

# global control objects.  These are all set by setConfig
ui_up = ui_down = ui_left = ui_right = ui_accept = ui_cancel = None
up = down = left = right = None
attack = cancel = rend = None
gale = heal = smoke = bolt = None
savestate = loadstate = None
showmap = None
speedhack= None

#baaad
allControls=[ui_up,ui_down,ui_left,ui_right,ui_accept,ui_cancel,
up,down,left,right,attack,cancel,rend,gale,heal,smoke,bolt,savestate,loadstate,showmap,speedhack]