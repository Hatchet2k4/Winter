
import ika

up = lambda: ika.Input.up.Pressed()
down = lambda: ika.Input.down.Pressed()
left = lambda: ika.Input.left.Pressed()
right = lambda: ika.Input.right.Pressed()
enter = lambda: ika.Input.enter.Pressed()
cancel = lambda: ika.Input.cancel.Pressed()

joy_up = lambda: ika.Input.up.Pressed()
joy_down = lambda: ika.Input.down.Pressed()
joy_left = lambda: ika.Input.left.Pressed()
joy_right = lambda: ika.Input.right.Pressed()
joy_enter = lambda: ika.Input.enter.Pressed()
joy_cancel = lambda: ika.Input.cancel.Pressed()

ui_up = lambda: ika.Input.up.Pressed()
ui_down = lambda: ika.Input.down.Pressed()
ui_left = lambda: ika.Input.left.Pressed()
ui_right = lambda: ika.Input.right.Pressed()
ui_accept = lambda: ika.Input.enter.Pressed()
ui_cancel = lambda: ika.Input.cancel.Pressed()