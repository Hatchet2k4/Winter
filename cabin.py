import ika
import controls
import savedata
import system

from xi import gui
from xi.misc import WrapText
from xi.scrolltext import ScrollableTextFrame
import xi.effects
import sound
import dir

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
    global grandpa, kid1, kid2, kid3, pl
    savedPos = [(e.x, e.y) for e in system.engine.entities]
    # hide 'em all
    for e in system.engine.entities:
        e.x, e.y = -100, -100


    ika.Map.Switch('maps/cabinmap.ika-map')
    grandpa = ika.Map.entities['grandpa']
    kid1 = ika.Map.entities['kid1']
    kid2 = ika.Map.entities['kid2']
    kid3 = ika.Map.entities['kid3']
    pl = system.engine.player

    xi.effects.fadeIn(50)

    _scenes[name]()
    setattr(savedata, name, 'True')

    xi.effects.fadeOut(50)

    grandpa = kid1 = kid2 = kid3 = None

    # FIXME? AutoExec will be called when you do this!
    if system.engine.mapName:
        ika.Map.Switch('maps/' + system.engine.mapName)
        for e, pos in zip(system.engine.entities, savedPos):
            e.x, e.y = pos
            system.engine.readEnts()
    system.engine.synchTime()
    

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
    narration("""Undaunted, he travelled ever-northward, the wintery air freezing in his throat. He needed only to traverse the treacherous Mount Durinar, his small village awaiting him on the other side.""")
    narration("""Though the bridges and roads built upon the mountain's cliffs had long since been abandoned to time, there were still stories told of lost magic, hidden somewhere within those frigid peaks.""")          
    narration("""As he climbed, the thoughts of enjoying a warm fire and hearty meal filled his head. But he was shocked out of his daydreams when suddenly...""")
    animate(kid3, (0, 1), delay=20, text="Oh no!!")
    narration("""The howls of a Razormane pack at the top of a steep hill startled him, and just as abruptly they began to give chase, moving swiftly and easily through the snow.""")
    narration("""His breaths came in chilled, raspy gasps as he ran. Even with his sword in hand, he knew he would be no match against the ravenous beasts.""")
    narration("""Before long, the pack pursued him right to the edge of a cliff. He turned to face his predators, but his boots lost their grip on the ice and he slipped.""")
    narration("""With an echoing scream, he fell, the sounds of stones crashing around him as he tumbled down into a ravine.""")    
    tint.tint = 0
    narration("""The Razormanes did not follow. The cliff face was far too steep to climb back up, and so they seemingly left him to his fate...""")

def story_water():   
    narration("""Somehow, he had managed to survive the return of the Razormane pack. It seemed there was something special about this place that made him stronger with every battle. """)    
    narration("""He looked down at the magical rune he now held, surrounded by wisps of vapor, and glowing with life giving power.""")
    narration("""Perhaps, he thought, this rune was one of the keys to finding his way through the labyrinth of these mountains.""")
 
    
    
def story_fire():
    narration("""The battle with the Yeti was fierce, but again the man prevailed. And for his trouble, he had discovered another rune.""")
    narration("""He could feel his sword's blade glowing with searing heat. Surely, this would allow him to open up new paths to explore. """)
   

def story_wind():      
    narration("""With another victory, he could feel both a physical and emotional weight lifting from his shoulders. He almost felt lighter than air.""") 
    narration("""His resolve growing, he believed that now there was nowhere he could not reach.""")
        

def nearend():    
    narration("""As he neared his journey's end, he once again began to grow tired, cold, and hungry. And yet, there were still more obstacles before him, ones that even his newfound powers could not breach.""")
    narration("""He considered... perhaps the only way forward, was to go back from whence he came.""")
    narration("""There must have been something he missed. Some clue he overlooked.""") 
    speech(kid1, 'Did he go back?')
    speech(kid2, 'Yeah!')
    speech(kid3, "He must have, he wouldn't have given up!!")    
    narration("""He had no choice. He would continue to search for some way forward. His desire to return home was unwavering... """)

def forebattle():
    narration("""As he felt the power of this last rune he had acquired, he knew that at last he had what he needed to continue. Finally, he could leave these lonely mountains and return home. """)
    narration("""He hoped there would be no further trials awaiting him... yet in his heart he believed that these cursed peaks were not quite done with him yet...""")


def epilogue(): 
    narration("""And so, finally, he could see the glowing windows and lit fires of his hometown. He had done it. It had taken all of his effort, but he had conquered the trials of that infernal place. """)
    speech(kid1, 'Yay!')
    speech(kid2, 'I knew he could do it!')
    speech(kid3, "Yeah, I wasn't worried at all!")
    speech(kid2, 'Wait a minute...')
    narration("""With a renewed sense of vigor and purpose, he descended. 
    
Finally, he could go home.""")
    wait(100)
    sound.step.Play()
    wait(10)
    pl.ent.x=7*16-8
    pl.ent.y=16*16    
    pl.direction=dir.UP
    pl.state = pl.cutsceneWalkState() 
    for i in range(56):        
        ika.ProcessEntities()
        pl.update()
        draw()
        ika.Video.ShowPage()
        wait(1)
    pl.stop()         
    pl.direction=dir.RIGHT
    
    pl._state = lambda: None
    pl.ent.specframe=20
    ika.ProcessEntities()
    draw()
    ika.Video.ShowPage()    
    speech((pl.ent.x, pl.ent.y-80), "I made it!")
   
    speech(kid2, 'Daddy!')
    speech(grandpa, "Welcome home, son!")
    speech((pl.ent.x, pl.ent.y-80), "You wouldn't believe what I had to go through to get back...")
    
#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

addScene(intro)
addScene(story_water)
addScene(story_fire)
addScene(story_wind)
addScene(nearend)
addScene(forebattle)
addScene(epilogue)
