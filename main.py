import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App

from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

import os
import sys
import json

# +----------------------------------+
# | StackLayout                      |
# | +------------------------------+ |
# | |Label                         | |
# | +------------------------------+ |
# | +------------------------------+ |
# | | ScrollView                   | |
# | | +----------------------+  ^  | |
# | | | StackLayout          | | | | |
# | | | +------------------+ | | | | |
# | | | |Label             | | | | | |
# | | | +------------------+ | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x|| Button        | | | | | |
# | | | +-++---------------+ | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x|| Button        | | | | | |
# | | | +-++---------------+ | | | | |
# | | | +------------------+ | | | | |
# | | | |Label             | | | | | |
# | | | +------------------+ | | | | |
# | | | ...                  | | | | |
# | | +----------------------+  v  | |
# | +------------------------------+ |
# | +------------------------------+ |
# | | BoxLayout                    | |
# | |     +-+ +------+ +---------+ | |
# | | Hide|x| | Undo | | Save    | | |
# | |     +-+ +------+ +---------+ | |
# | +------------------------------+ |
# +----------------------------------+

class CheckList(StackLayout):

    def __init__(self, **kwargs):
        super(CheckList, self).__init__(**kwargs)

        if 'HOME' in os.environ:
            dataDir = os.environ['HOME'] + '/.config/Checker/'
        else:
            dataDir = '/sdcard/Android/data/se.jonaseel.checker/files'

        try:
            with open(dataDir + '/Checker.json') as fd:
                    shoppingList=json.load(fd)
        except:
            shoppingList = [
              {"section": "Section 1", "items": [
                {"item": "Item 1", "done": False},
                {"item": "Item 2", "done": True},
                {"item": "Item 3", "done": True}
              ]},
              {"section": "Section 2", "items": [
                {"item": "Item 1", "done": True},
                {"item": "Item 2", "done": False},
                {"item": "Item 3", "done": False},
                {"item": "Item 4", "done": True}
              ]},
              {"section": "Section 3", "items": [
                {"item": "Item 1", "done": True},
                {"item": "Item 2", "done": True},
                {"item": "Item 3", "done": False}
              ]}
            ]

        defaultSettings = {
            'headerSize': '10sp',
            'sectionSize': '20sp',
            'sectionTextSize': '10sp',
            'labelSize': '30sp',
            'doneColor': [0, 1, 0, 1],
        }
        try:
            with open(dataDir + '/settings.json') as fd:
                    settings=json.load(fd)
                    for key in defaultSettings:
                        if not key in settings:
                            settings[key] = defaultSettings[key]
        except:
            settings = defaultSettings

        def hide(widget):
            widget.height = 0
            widget.opacity = 0
            widget.disabled = True

        def unhide(widget):
            widget.height = settings['labelSize']
            widget.opacity = 1
            widget.disabled = False

        def populate(stack, shoppingList):
            for section in shoppingList:
                sectionLabel = Button(
                        text=section['section'].upper(),
                        font_size=settings['sectionTextSize'],
                        height=settings['sectionSize'],
                        size_hint=(1, None),
                        markup=True,
                )
                stack.add_widget(sectionLabel)
                for item in section['items']:
                    label = Button(
                        text=item['item'],
                        height=settings['labelSize'],
                        size_hint=(0.95, None),
                    )
                    label.section = section
                    label.sectionLabel = sectionLabel
                    label.data = item
                    label.bind(on_release = toggle)
                    check = CheckBox(
                        height=title.height,
                        size_hint=(0.05, None),
                    )
                    if label.data['done']:
                          label.background_color = settings['doneColor']
                          check.state = 'down'
                    check.label = label
                    label.check = check
                    check.bind(on_release = crossCheck)
                    stack.add_widget(check)
                    stack.add_widget(label)

        def checkSection(stack, current):
            isEmpty = True
            for item in current.section['items']:
                if not item['done']:
                    isEmpty = False
                    break
            if isEmpty:
                hide(current.sectionLabel)

        self.writeDeferred = False
        def deferWrite(dt):
            self.writeDeferred = False
            with open(dataDir + '/Checker.json', 'w') as fd:
                json.dump(shoppingList, fd)
            print("shoppingList saved")

        def toggle(instance):
            if instance.data['done']:
                instance.data['done'] = False
                instance.background_color = [1,1,1,1]
                instance.check.state = 'normal'
            else:
                instance.data['done'] = True
                instance.background_color = settings['doneColor']
                instance.check.state = 'down'

            if not self.writeDeferred:
                self.writeDeferred = True
                Clock.schedule_once(deferWrite, 1)

            if self.hide.state == 'down' and instance.data['done']:
                hide(instance.check)
                hide(instance)
                checkSection(stack, instance)

        def hideUnHide(instance):
            if instance.state == "down":
                hasChildren = False
                for item in stack.children[:]:
                    if isinstance(item, Button):
                        try:
                            if item.data['done']:
                                hide(item.check)
                                hide(item)
                            else:
                                hasChildren = True
                        except:
                            if not hasChildren:
                                hide(item)
                            hasChildren = False
            else:
                for item in stack.children[:]:
                    unhide(item)

        def crossCheck(instance):
            toggle(instance.label)

        title = Label(
            text='Checker',
            size_hint=(1, .05),
            height = settings['headerSize'],
        )
        self.add_widget(title)

        scrollBox = ScrollView(
            size_hint=(1, .9),
            do_scroll_x=False,
        )
        self.add_widget(scrollBox)

        stack = StackLayout(size_hint=(1, None))
        stack.bind(
            minimum_height=stack.setter('height')
        )
        scrollBox.add_widget(stack)

        populate(stack, shoppingList)

        buttons = BoxLayout(
            size_hint=(1, .05)
        )
        self.add_widget(buttons)
        buttons.add_widget(
            Label(
                text="Hide:",
                size_hint=(None, 1)
            ))
        self.hide = CheckBox(
                on_release=hideUnHide,
                size_hint=(None, 1),
            )
        buttons.add_widget(self.hide)
        buttons.add_widget(
            Button(
                text="Quit",
                on_release=exit,
                size_hint=(1, 1),
            ))

class Checker(App):

    def build(self):
        return CheckList()

if __name__ == '__main__':
    Checker().run()
