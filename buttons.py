import kivy
kivy.require('1.11.0') # replace with your current kivy version !

from kivy.factory import Factory
from kivy.clock import Clock

from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

class ToggleImageButton(ToggleButtonBehavior, Image):
    image_normal = Factory.StringProperty('atlas://data/images/defaulttheme/checkbox_off')
    image_down = Factory.StringProperty('atlas://data/images/defaulttheme/checkbox_on')
    color_normal = Factory.ListProperty([1, 1, 1, 1])
    color_down = Factory.ListProperty([1, 1, 1, .6])
    color_active = Factory.ListProperty([.2, .7, .9, 1])

    def __init__(self, **kwargs):
        super(ToggleImageButton, self).__init__(**kwargs)
        self.source = self.image_normal
        self.color = self.color_normal

    def on_state(self, widget, value):
        if value == 'down':
            self.source = self.image_down
            self.color = self.color_active
        else:
            self.source = self.image_normal
            self.color = self.color_active

    def on_release(self):
        if self.state == 'down':
            self.color = self.color_down
        else:
            self.color = self.color_normal

class ImageButton(ButtonBehavior, Image):
    color_normal = Factory.ListProperty([0, 0, 0, 0])
    color_down = Factory.ListProperty([.2, .7, .9, 1])

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.color = self.color_normal
        self.always_release = True

    def on_press(self):
        self.color = self.color_down

    def on_release(self):
        self.color = self.color_normal

class LongpressButton(Factory.Button):
    __events__ = ('on_long_press', 'on_short_press')

    long_press_time = Factory.NumericProperty(0.2)
    background_normal = ''

    def on_state(self, instance, value):
        lpt = self.long_press_time
        if value == 'down':
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            if self._clockev.is_triggered:
                self._clockev.cancel()
                self.dispatch('on_short_press')

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass

    def on_short_press(self, *largs):
        pass

class LongpressImageButton(Factory.ImageButton):
    __events__ = ('on_long_press', 'on_short_press')

    long_press_time = Factory.NumericProperty(0.2)
    color_normal = Factory.ListProperty([0, 0, 0, 0])
    color_down = Factory.ListProperty([.2, .7, .9, 1])

    def on_state(self, instance, value):
        lpt = self.long_press_time
        if value == 'down':
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            if self._clockev.is_triggered:
                self._clockev.cancel()
                self.dispatch('on_short_press')

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass

    def on_short_press(self, *largs):
        pass
