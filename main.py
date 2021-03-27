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
# | | | +------------------+ | | | | |
# | | | |Button            | | | | | |
# | | | +------------------+ | | | | |
# | | | +------------------+ | | | | |
# | | | |Button            | | | | | |
# | | | +------------------+ | | | | |
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

        def toggle(instance):
            print(instance.section)
            if instance.done:
                instance.done = False
                instance.background_color = [1,1,1,1]
            else:
                instance.done = True
                instance.background_color = [0,0,1,1]
            if self.hide.state == 'down' and instance.done:
                stack.remove_widget(instance)

        def update(instance):
            if instance.state == "down":
                for item in stack.children[:]:
                    try:
                        if item.done:
                            stack.remove_widget(item)
                    except: pass
            else:
                print("not implemented")

        title = Label(
            text='Checker',
            size_hint=(1, .05),
            height = '30sp',
        )
        self.add_widget(title)

        shoppingList=json.load(open('Checker.json'))

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

        for section in shoppingList:
            stack.add_widget(
                Label(
                    text=section['section'],
                    height=title.height,
                    size_hint=(1, None),
                ))
            for item  in section['items']:
                label = Button(
                        text=item['item'],
                        height=title.height,
                        size_hint=(1, None),
                    )
                label.section = section['section']
                label.done = item['done']
                if label.done:
                      label.background_color = [0,0,1,1]
                label.bind(on_release = toggle)
                stack.add_widget(label)

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
                on_release=update,
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


