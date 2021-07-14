'''
Input abstraction and so on.
'''

import ika

from keynames import keyNames
import controls
import xi.controls

from saveload import SaveGame

# Name : Control pairs
_allControls = dict()


defaultControls = {
    'up': 'UP',
    'down': 'DOWN',
    'left': 'LEFT',
    'right': 'RIGHT',
    'attack': 'SPACE',
    'cancel': 'ESCAPE',
    'rend': 'Z',
    'gale': 'X',
    'heal': 'C',
    'smoke': 'V',
    'shiver': 'B',
    'vivify': 'N',
    'ternion': 'M',
    'savestate': 'F2',
    'loadstate': 'F4',
    'showmap': 'TAB',
    'speedhack': 'Q'
}
displayControls = {}

#joystick friendly names
#_friendlyNames = dict()

def init():
    # fill up _allControls

    # Null control
    _allControls['none'] = lambda: False

    # keyboard keys:
    for k in keyNames:
        _allControls[k] = ika.Input.keyboard[k]

    

    # joystick:
    for joyIndex, joy in enumerate(ika.Input.joysticks):
        # axes:
        for axisIndex, axis in enumerate(joy.axes):
            _allControls['joy%iaxis%i+' % (joyIndex, axisIndex)] = axis
            #_friendlyNames['joy%ibutton%i' % (joyIndex, axisIndex)] = 'JoyAxis:'+str(axisIndex)
        for axisIndex, axis in enumerate(joy.reverseAxes):
            _allControls['joy%iaxis%i-' % (joyIndex, axisIndex)] = axis
            #_friendlyNames['joy%ibutton%i' % (joyIndex, axisIndex)] = 'JoyAxis:'+str(axisIndex)

        # buttons:
        for buttonIndex, button in enumerate(joy.buttons):
            _allControls['joy%ibutton%i' % (joyIndex, buttonIndex)] = button
            #_friendlyNames['joy%ibutton%i' % (joyIndex, buttonIndex)] = 'Joy:'+str(buttonIndex)

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

def setConfig(config=None):
    class PosControl(object):
        def __init__(self, name):
            self.name = name
            self.c = _allControls[config[name]]
            
            if config[name][0:3] == 'joy': #dealing with a gamepad                        
                displayControls[name] = config[name][-1] #haaack, just grab last character. will break if more than 10 buttons..                
            else:
                displayControls[name] = config[name]
        def __call__(self):   return self.c.Position() > 0
        def __repr__(self):   return '<Winter control %s>' % self.name

    class PressControl(PosControl):
        def __call__(self):
            return self.c.Pressed()

    if config is None:
        config = defaultControls
    # Directional controls:
    for name in ('up', 'down', 'left', 'right'):
        globals()[name] = PosControl(name)

    # Buttons
    for name in ('attack', 'cancel', 'rend',
                 'gale', 'heal', 'smoke',
                 'shiver', 'vivify', 'ternion', 
                 'savestate', 'loadstate', 'showmap', 'speedhack'):
        globals()[name] = PressControl(name)
    

    # Copy controls over to xi.
    for c in ('up', 'down', 'left', 'right'):
        setattr(xi.controls, c, getattr(controls, c))
    xi.controls.enter = controls.attack
    xi.controls.cancel = controls.cancel
    
    #displayControls=config
    #ika.Log(str(config))

    

# global control objects.  These are all set by setConfig
up = down = left = right = None
attack = cancel = rend = None
gale = heal = smoke = shiver = None
savestate = loadstate = None
showmap = None
speedhack= None