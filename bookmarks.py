import kivy
kivy.require('1.11.0') # replace with your current kivy version !

from kivy.factory import Factory

from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

import os, re
from glob import glob
from datetime import datetime, timedelta

from buttons import ImageButton, LongpressButton, LongpressImageButton

class BookmarkList(BoxLayout):
    dataDir = Factory.StringProperty('.')
    settings = Factory.DictProperty({})
    chosen = Factory.StringProperty('')

    def __init__(self, **kwargs):
        super(BookmarkList, self).__init__(**kwargs)

        scrollBox = ScrollView(
            do_scroll_x=False,
        )
        self.add_widget(scrollBox)

        stack = StackLayout(size_hint=(1, None))
        stack.bind(
            minimum_height=stack.setter('height')
        )
        scrollBox.add_widget(stack)

        bookmarks = sorted(glob(f'{self.dataDir}/bookmarks/*.json'), key = os.path.getmtime)[::-1]
        for filename in bookmarks:
            bookmark = filename[len(f'{self.dataDir}/bookmarks/'):-5]
            label = LongpressButton(
                text = bookmark,
                height = self.settings['labelSize'],
                background_color = self.settings['sectionColor'],
                size_hint = (1, None),
                on_long_press = lambda w: edit(w),
                on_short_press = lambda w: choose(w)
            )
            label.selected = False
            stack.add_widget(label)

        buttonBar = BoxLayout()
        self.add_widget(buttonBar)
        cancelBtn = ImageButton(
            source = 'data/delete.png',
            color_normal = self.settings['inactiveColor'],
            size_hint = (1, None),
            height = self.settings['headerSize'],
            on_release = lambda w: self.parent.parent.parent.dismiss(),
        )
        deleteBtn = ImageButton(
            source = 'data/trash.png',
            color_normal = self.settings['inactiveColor'],
            size_hint = (1, None),
            height = self.settings['headerSize'],
            on_release = lambda w: deleteSelected(),
        )
        buttonBar.add_widget(deleteBtn)
        buttonBar.add_widget(cancelBtn)

        def choose(item):
            selection = False
            for sibling in item.parent.children:
                if sibling.selected:
                    selection = True
                    break
            if selection:
                if item.selected:
                    deselect(item)
                else:
                    select(item)
            else:
                self.chosen = item.text
                self.parent.parent.parent.dismiss()

        def edit(w):
            editBox = BoxLayout(
                height = self.settings['labelSize'],
                size_hint = (1, None),
            )
            entry = TextInput(
                text = w.text,
                multiline = False,
                on_text_validate = lambda w: updateItem(w),
            )
            delete = ImageButton(
                size_hint_x = None,
                width = self.settings['labelSize'],
                source = 'data/trash.png',
                color_normal = self.settings['actionColor'],
                on_release = lambda w: selectItem(entry),
            )
            ok = ImageButton(
                size_hint_x = None,
                width = self.settings['labelSize'],
                source = 'data/ok.png',
                color_normal = [0, .5, 0, 1],
                on_release = lambda w: updateItem(entry),
            )
            editBox.add_widget(delete)
            editBox.add_widget(entry)
            editBox.add_widget(ok)

            entry.index = stack.children.index(w)
            entry.orig = w
            stack.add_widget(editBox, entry.index)
            stack.remove_widget(w)

        def remove_widgets(entry):
            for item in entry.children:
                entry.remove_widget(item)
            entry.parent.remove_widget(entry)

        def updateItem(entry):
            os.rename(f'{self.dataDir}/bookmarks/{entry.orig.text}.json', f'{self.dataDir}/bookmarks/{entry.text}.json')
            entry.orig.text = entry.text
            stack.add_widget(entry.orig, entry.index)
            remove_widgets(entry.parent)

        def selectItem(entry):
            stack.add_widget(entry.orig, entry.index)
            select(entry.orig)
            remove_widgets(entry.parent)
            deleteBtn.color = self.settings['redColor']

        def select(item):
            item.selected = True
            item.background_color = self.settings['actionColor']

        def deselect(item):
            item.selected = False
            item.background_color = self.settings['sectionColor']

        def deleteSelected():
            for item in stack.children[:]:
                if item.selected:
                    os.remove(f'{self.dataDir}/bookmarks/{item.text}.json')
                    stack.remove_widget(item)
