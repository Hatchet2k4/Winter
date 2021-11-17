import ika
import controls
import savedata
import system

from xi import gui
from xi.misc import WrapText
from xi.scrolltext import ScrollableTextFrame
import xi.effects
import sound

#------------------------------------------------------------------------------

controls.init()

class Tinter(object):
    def __init__(self):
        self.curTint = 0
        self.tint = 0
        self.time = 0

    def draw(self):
        self.curTint += self.curTint < self.tint
        self.curTint -= self.curTint > self.tint

        if self.curTint:
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, self.curTint), True)

tint = Tinter()

crap = [tint] # crap to draw along with the map

def draw():
    ika.Map.Render()
    for c in crap:
        c.draw()

#------------------------------------------------------------------------------

def textBox(where, txt):
    # where is either a point or an entity
    WIDTH = 200
    width = WIDTH
    text = WrapText(txt, width, gui.default_font)
    width = max([gui.default_font.StringWidth(s) for s in text])
    height = len(text) * gui.default_font.height

    if isinstance(where, ika.Entity):
        ent = where
        x, y = ent.x + ent.hotwidth / 2 - ika.Map.xwin, ent.y - ika.Map.ywin
    else:
        x, y = where

    if x < ika.Video.xres / 2:
        x -= width / 2

    width = WIDTH
    if x + width + 16 > ika.Video.xres:
        text = WrapText(txt, ika.Video.xres - x - 16, gui.default_font)
        width = max([gui.default_font.StringWidth(s) for s in text])
        height = len(text) * gui.default_font.height

    frame = ScrollableTextFrame()
    frame.addText(*text)
    frame.autoSize()

    if y > ika.Video.yres / 2:
        y += 32
    else:
        y -= frame.Height + 16

    frame.Position = x, y
    return frame

#------------------------------------------------------------------------------

def text(where, txt):
    """Displays a text frame.

    Where can be either a point or an ika entity.
    """
    frame = textBox(where, txt)

    while not (controls.attack() or controls.joy_attack() or controls.ui_accept()):
        draw()
        frame.draw()
        ika.Video.ShowPage()
        ika.Input.Update()

def wait(duration): 
    t = ika.GetTime()
    d = t+duration
    while t < d:
        draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        t = ika.GetTime()

#------------------------------------------------------------------------------

def animate(ent, frames, delay, thing=None, loop=True, text=None):
    class AnimException(Exception):
        pass
    # frames should be a list of (frame, delay) pairs.
    if thing is not None:
        crap.append(thing)
    if text is not None:
        text = textBox(ent, text)
        crap.append(text)
    try:
        while True:
            for frame in frames:
                ent.specframe = frame
                d = delay
                while d > 0:
                    d -= 1
                    draw()
                    ika.Video.ShowPage()
                    ika.Delay(1)
                    ika.Input.Update()
                    if controls.attack() or controls.ui_accept() or controls.joy_attack():
                        loop = False
                        raise AnimException
            if not loop:
                raise AnimException
    except:  #except what?
        if thing:
            crap.remove(thing)
        if text:
            crap.remove(text)
        ent.specframe = 0

#------------------------------------------------------------------------------
# Scene code
#------------------------------------------------------------------------------

_scenes = {}

# TODO: transitions
def scene(name):
    global grandpa, kid1, kid2, kid3
    savedPos = [(e.x, e.y) for e in system.engine.entities]
    # hide 'em all
    for e in system.engine.entities:
        e.x, e.y = -100, -100

    ika.Map.Switch('maps/cabinmap.ika-map')
    grandpa = ika.Map.entities['grandpa']
    kid1 = ika.Map.entities['kid1']
    kid2 = ika.Map.entities['kid2']
    kid3 = ika.Map.entities['kid3']

    xi.effects.fadeIn(100)

    _scenes[name]()
    setattr(savedata, name, 'True')

    xi.effects.fadeOut(100)

    grandpa = kid1 = kid2 = kid3 = None

    # FIXME? AutoExec will be called when you do this!
    if system.engine.mapName:
        ika.Map.Switch('maps/' + system.engine.mapName)
        for e, pos in zip(system.engine.entities, savedPos):
            e.x, e.y = pos

# name : function pairs
def addScene(function):
    _scenes[function.__name__] = function

#------------------------------------------------------------------------------
# Ear's functions
#------------------------------------------------------------------------------

PAUSE = 0
SPEAKING = 1
NOD = 2

TALKING = (
    [PAUSE]*3 +
    [SPEAKING]*2 +
    [PAUSE]*3 +
    [SPEAKING]*2 +
    [PAUSE]*3 +
    [NOD]
)

speech = text
narration = lambda t: animate(grandpa, TALKING, 25, text=t)

#------------------------------------------------------------------------------
# Scenes
#------------------------------------------------------------------------------

def intro():
    sound.playMusic('music/Wind.ogg')   
    wait(75)
    speech(grandpa, "It's getting to be quite the blizzard out there...")
    wait(75)
    animate(kid1, (0, 1), delay=20, text='Oh no! I hope daddy will be able to get back here?')
    speech(grandpa, "Oh, he'll be fine. We grew up in these mountains, this is nothing for him.")
    animate(kid1, (0, 1), delay=20, text="Ok, if you're sure!")
    wait(75)
    speech(grandpa, "While we wait, why don't I tell you a story?")    
    animate(kid3, (0, 1), delay=20, text='Yeah! Tell us a story!')
    animate(kid2, (1,), delay=20, text='How about the one about the ice man?')
    animate(kid1, (0, 1), delay=20, text="Yeah!")
    speech(grandpa, "Isn't that story a little scary?")
    animate(kid1, (0, 1), delay=20, text='No!')
    animate(kid2, (0, 1), delay=20, text='Please tell us!')
    speech(grandpa, 'Oh all right.  Ahem.')
    animate(kid3, (0, 1), delay=20, text="I'm a little scared...")

    tint.tint = 200

    narration("""Across the frozen hills of the province of Kuladriat, a simple man was returning home from a long journey. Even dressed in his warmest cloak, he could feel the stinging wind chilling him right down to his bones.""")
    narration("""Undaunted, he travelled ever-northward. He needed only to traverse the treacherous Mount Durinar. He knew that his little village he called home awaited him on the other side.""")
    narration("""Though the bridges and roads built upon the mountain's cliffs had long since been abandoned to time, there were still stories told of lost magic, hidden somewhere within those frigid peaks.""")          
    narration("""As he climbed, the thoughts of enjoying a warm fire and hearty meal filled his head. But he was shocked out of his daydreams when suddenly...""")

    animate(kid3, (0, 1), delay=20, text="Oh no!!")

    narration("""The howls of a razormane pack at the top of a steep hill startled him, and just as abruptly they began to give chase, moving swiftly and easily through the snow.""")

    narration("""The cold air felt sharp in his throat as he ran. Even with his sword in hand, he knew he would be no match against the ravenous beasts.""")

    narration("""He was forced to flee, and the pack pursued him right to the edge of a cliff. Before he could stop himself, his boots lost their grip on the ice, and he tumbled down into a ravine.""")
    
    tint.tint = 0

    narration("""They did not follow. The cliff face was far too steep to climb back up, and so they left him to his fate...""")



def impasse():
    narration("""\
The stone walls seemed to draw in closer, choking the very breath \
from him; the way was sealed.  However, as despair welled within \
him, a glint of hope shone through as light through the gelid rock.  \
If only there were some way to breach it...""")



def nearend():
    
    tint.tint = 200    
    narration("""As he neared his journey's end, he grew even more tired, cold, and hungry. And yet, there were still more obstacles before him, ones that even his newfound power could not breach. """)


    narration("""He considered... perhaps the only way forward, was to go back from whence he came.""")

    narration("""There must have been something he missed. Perhaps if he returned to where he found the runes he carried, there may be some clue.""")

    tint.tint = 0
    
    speech(kid1, 'Did he go back?')
    speech(kid2, 'Yeah!')
    speech(kid3, "He must have, he wouldn't have given up!!")
    
    narration("""He had no choice. He would continue to search the mountain for some way forward. His desire to return home was unwavering... """)

def forebattle():
    tint.tint = 200    
    narration("""As he held the final rune above his head, he knew that he finally had the power to continue. The power to leave these lonely mountains and return home. """)

    narration("""He hoped there would be no further trials awaiting him... yet knew in his heart that these cursed peaks were not done with him yet...""")

    tint.tint = 0

def epilogue():
    tint.tint = 0    
    narration("""And so, he finally, could see the glwoing windows and lit fires of his hometown. He had done it. It had taken all of his effort, but he had conquered the trials this infernal place had left him. """)
    speech(kid1, 'Yay!')
    speech(kid2, 'I knew he could do it!')
    speech(kid3, "Yeah, I wasn't worried at all!")
    speech(kid2, 'Wait a minute...')
    narration("""With a renewed sense of vigor and purpose, he descended. 
    
Finally, he could go home.""")

   
def story_4():
    tint.tint = 200    
    narration("""Somehow, he had managed to survive the return of the razormane pack. There was something magical about this place that seemed to make him stronger with every battle he fought. """)
    narration("""He looked at the magical rune he now held, that seemed surrounded by chilled vapors, and yet also glowed with a life giving power. Perhaps, he thought, these runes were the key to escaping these mountains...""")
    tint.tint = 0    
#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

addScene(intro)
addScene(story_4)
#addScene(rune_of_fire)
#addScene(rune_of_wind)
#addScene(impasse)
addScene(nearend)
addScene(forebattle)
addScene(epilogue)
