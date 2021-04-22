import kivy
kivy.require('1.11.0') # replace with your current kivy version !

from kivy.factory import Factory

from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

import os, re
from glob import glob
from datetime import datetime, timedelta

from buttons import ToggleImageButton, ImageButton, LongpressButton, LongpressImageButton

class BookmarkList(StackLayout):
    dataDir = Factory.StringProperty('.')
    settings = Factory.DictProperty({})
    chosen = Factory.StringProperty('')

    def __init__(self, **kwargs):
        super(BookmarkList, self).__init__(**kwargs)

        scrollBox = ScrollView(
            size_hint=(1, 0.95),
            do_scroll_x=False,
        )
        self.add_widget(scrollBox)

        stack = StackLayout(size_hint=(1, None))
        stack.bind(
            minimum_height=stack.setter('height')
        )
        scrollBox.add_widget(stack)

        bookmarks = sorted(glob(f'{self.dataDir}/*.json'), key = os.path.getmtime)
        for filename in bookmarks:
            if re.search(f'{self.dataDir}/(Plocka.*|settings).json', filename):
                continue
            bookmark = filename[len(f'{self.dataDir}/'):-5]
            label = LongpressButton(
                text = bookmark,
                height = self.settings['labelSize'],
                background_color = self.settings['sectionColor'],
                size_hint = (1, None),
                on_long_press = lambda w: edit(w),
                on_short_press = lambda w: choose(w.text)
            )
            stack.add_widget(label)

        buttons = BoxLayout(
            size_hint=(1, None)
        )
        self.add_widget(buttons)

        cancelBtn = ImageButton(
            source = 'data/undo.png',
            color_normal = [1, 0, 0, 0.5],
            size_hint = (1, None),
            height = self.settings['headerSize'],
            on_release = lambda w: self.parent.parent.parent.dismiss(),
        )
        buttons.add_widget(cancelBtn)

        def choose(text):
            self.chosen = text
            self.parent.parent.parent.dismiss()

        def edit(w):
            pass
