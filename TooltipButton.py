from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button


class TooltipButton(Button):

    def __init__(self, **kwargs):
        super(TooltipButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.collide_point(*pos):
            Clock.schedule_once(self.mouse_enter, 0)
        else:
            Clock.schedule_once(self.mouse_leave, 0)

    def mouse_leave(self, *args):
        self.callback(self.order, False)

    def mouse_enter(self, *args):
        self.callback(self.order, True)
