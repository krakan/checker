import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.base import runTouchApp
from kivy.factory import Factory
from kivy.clock import Clock

from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.label import Label

import os
import sys
import json
from glob import glob
from datetime import datetime, timedelta


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

class LongpressButton(Factory.Button):
    __events__ = ('on_long_press', 'on_short_press')

    long_press_time = Factory.NumericProperty(0.2)

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

class CheckList(StackLayout):

    def __init__(self, **kwargs):
        super(CheckList, self).__init__(**kwargs)

        if 'HOME' in os.environ:
            dataDir = os.environ['HOME'] + '/.config/Checker'
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
            'sectionColor': [0,.5,0,1],
            'sectionTextSize': '10sp',
            'labelSize': '30sp',
            'doneColor': [0, 1, 0, 1],
            'backupsToKeep': 10,
            'maxBackupAge': 1,
        }
        try:
            with open(dataDir + '/settings.json') as fd:
                    settings=json.load(fd)
                    for key in defaultSettings:
                        if not key in settings:
                            settings[key] = defaultSettings[key]
        except:
            settings = defaultSettings

        backups = sorted(glob(f'{dataDir}/Checker-*.json'))
        cutoff = (datetime.now() - timedelta(days=settings['maxBackupAge'])).strftime("%Y%m%d%H%M%S")
        for backup in backups[:-settings['backupsToKeep']]:
            if backup < f'{dataDir}/Checker-{cutoff}.json':
                print('deleting backup file ' + backup)
                os.remove(backup)

        def hide(widget):
            widget.restore = widget.height
            widget.height = 0
            widget.opacity = 0
            widget.disabled = True

        def unhide(widget):
            if widget.disabled:
                widget.height = widget.restore
                widget.opacity = 1
                widget.disabled = False

        def populate(stack, shoppingList):
            stack.clear_widgets()
            for section in shoppingList:
                sectionLabel = Button(
                        text=section['section'].upper(),
                        font_size=settings['sectionTextSize'],
                        height=settings['sectionSize'],
                        background_color=settings['sectionColor'],
                        size_hint=(1, None),
                        markup=True,
                )
                stack.add_widget(sectionLabel)
                for item in section['items']:
                    label = LongpressButton(
                        text=item['item'],
                        height=settings['labelSize'],
                        size_hint=(0.95, None),
                        on_short_press=lambda w: toggle(w),
                        on_long_press=lambda w: edit(w),
                    )
                    label.section = section
                    label.sectionLabel = sectionLabel
                    check = CheckBox(
                        height=settings['labelSize'],
                        size_hint=(0.05, None),
                        on_release=lambda w: crossCheck(w),
                    )
                    if item['done']:
                          label.background_color = settings['doneColor']
                          check.state = 'down'
                    check.label = label
                    label.check = check
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
        def writeFile(dt):
            self.writeDeferred = False
            shoppingList = []
            for item in stack.children[::-1]:
                if isinstance(item, Button):
                    try:
                        entry = {
                            "item": item.text,
                            "done": item.check.state == 'down'
                        }
                        section["items"].append(entry)
                    except:
                        section = {
                            "section": item.text,
                            "items": []
                        }
                        shoppingList.append(section)

            now = datetime.now().strftime("%Y%m%d%H%M%S")
            os.rename(f'{dataDir}/Checker.json', f'{dataDir}/Checker-{now}.json')
            with open(f'{dataDir}/Checker.json', 'w', encoding='utf8') as fd:
                json.dump(shoppingList, fd, indent=2, ensure_ascii=False)

        def undo(instance):
            try:
                last = sorted(glob(f'{dataDir}/Checker-*.json'))[-1]
                os.rename(last, f'{dataDir}/Checker.json')
                with open(dataDir + '/Checker.json') as fd:
                        shoppingList=json.load(fd)
                populate(stack, shoppingList)
                hideUnHide(self.hide)
            except: pass

        def toggle(instance):
            if instance.check.state == 'down':
                instance.background_color = [1,1,1,1]
                instance.check.state = 'normal'
            else:
                instance.background_color = settings['doneColor']
                instance.check.state = 'down'

            if not self.writeDeferred:
                self.writeDeferred = True
                Clock.schedule_once(writeFile, 1)

            if self.hide.state == 'down' and instance.check.state == 'down':
                hide(instance.check)
                hide(instance)
                checkSection(stack, instance)

        def hideUnHide(instance):
            if instance.state == "down":
                hasChildren = False
                for item in stack.children[:]:
                    if isinstance(item, Button):
                        try:
                            if item.check.state == 'down':
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

        def edit(instance):
            entry = TextInput(
                text = instance.text,
                size_hint = (0.5, None),
                height = settings['labelSize'],
                multiline = False,
                on_text_validate = lambda w: save(w),
            )
            before = Button(
                text = '^',
                height = settings['labelSize'],
                size_hint = (0.125, None),
                on_press = lambda w: save(entry),
            )
            replace = Button(
                text = 'o',
                height = settings['labelSize'],
                size_hint = (0.125, None),
                on_press = lambda w: save(entry),
            )
            after = Button(
                text = 'v',
                height = settings['labelSize'],
                size_hint = (0.125, None),
                on_press = lambda w: save(entry),
            )
            delete = Button(
                text = 'x',
                background_color = [1, 0, 0, 1],
                height = settings['labelSize'],
                size_hint = (0.125, None),
                on_press = lambda w: save(entry),
            )
            entry.orig = instance
            entry.before = before
            entry.replace = replace
            entry.after = after
            entry.delete = delete

            hide(instance)
            hide(instance.check)
            index = stack.children.index(instance)
            stack.add_widget(delete, index)
            stack.add_widget(entry, index)
            stack.add_widget(before, index)
            stack.add_widget(replace, index)
            stack.add_widget(after, index)

        def save(entry):
            todo = 'replace'
            if entry.delete.state == 'down':
                todo = 'delete'
            elif entry.before.state == 'down':
                todo = 'before'
            elif entry.after.state == 'down':
                todo = 'after'
            text = entry.text
            orig = entry.orig

            stack.remove_widget(entry.before)
            stack.remove_widget(entry.replace)
            stack.remove_widget(entry.after)
            stack.remove_widget(entry.delete)
            stack.remove_widget(entry)

            if todo == 'delete':
                stack.remove_widget(orig)
                stack.remove_widget(orig.check)
            else:
                unhide(orig)
                unhide(orig.check)
                if todo == 'before' or todo == 'after':
                    label = LongpressButton(
                        text = text,
                        height=settings['labelSize'],
                        size_hint=(0.95, None),
                        on_short_press=lambda w: toggle(w),
                        on_long_press=lambda w: edit(w),
                    )
                    label.section = orig.section
                    label.sectionLabel = orig.sectionLabel
                    check = CheckBox(
                        height=settings['labelSize'],
                        size_hint=(0.05, None),
                        on_release=lambda w: crossCheck(w),
                    )
                    check.label = label
                    label.check = check
                    index = stack.children.index(orig)
                    if todo == 'before':
                        index += 2
                    stack.add_widget(check, index)
                    stack.add_widget(label, index)
                    if orig.check.state == 'down':
                        toggle(label)
                else:
                    orig.text = text

            writeFile(1)

        # MAIN

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
                text="Undo",
                on_release=undo,
                size_hint=(1, 1),
            ))
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
