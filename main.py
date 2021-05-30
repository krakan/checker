import kivy
kivy.require('1.11.0') # replace with your current kivy version !

from kivy.app import App
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.utils import platform

from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument

import os, sys, json, re, time, shutil
from glob import glob
from datetime import datetime, timedelta

from bookmarks import BookmarkList
from buttons import ToggleImageButton, ImageButton, LongpressButton, LongpressImageButton

__version__ = '1.6.1'

# +----------------------------------+
# | +------------------------------+ |
# | | +---------------+ +--------+ | |
# | | | Title         | | Search | | |
# | | +---------------+ +--------+ | |
# | +------------------------------+ |
# | +------------------------------+ |
# | | +----------------------+  ^  | |
# | | | +------------------+ | | | | |
# | | | | Section 1        | | | | | |
# | | | +------------------+ | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x|| Item 1        | | | | | |
# | | | +-++---------------+ | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x|| Item 2        | | | | | |
# | | | +-++---------------+ | | | | |
# | | | +------------------+ | | | | |
# | | | | Section 2        | | | | | |
# | | | +------------------+ | | | | |
# | | | ...                  | | | | |
# | | +----------------------+  v  | |
# | +------------------------------+ |
# | +------------------------------+ |
# | | +------+ +------+ +--------+ | |
# | | | Hide | | Undo | | Bookm. | | |
# | | +------+ +------+ +--------+ | |
# | +------------------------------+ |
# +----------------------------------+

class CheckList(BoxLayout):

    def __init__(self, **kwargs):
        super(CheckList, self).__init__(**kwargs)

        if platform == "android":
            from android.storage import primary_external_storage_path
            from android.permissions import request_permissions, check_permission, Permission

            sdcard = primary_external_storage_path()
            dataDir = sdcard + '/plocka'

            if not os.path.exists(dataDir):
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
                while not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                    time.sleep(1)
        else:
            dataDir = os.environ['HOME'] + '/.config/Plocka'

        os.makedirs(dataDir, exist_ok=True)

        scriptDir = os.path.dirname(os.path.realpath(__file__))

        global shoppingList
        try:
            with open(dataDir + '/Plocka.json') as fd:
                    shoppingList = json.load(fd)
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
            'headerSize': '40sp',
            'sectionSize': '20sp',
            'sectionColor': [0.1, 0.2, 0.2, 1],
            'sectionTextSize': '10sp',
            'itemSize': '30sp',
            'itemColor': [0.20, 0.25, 0.29, 1],
            'doneColor': [0.24, 0.30, 0.35, 1],
            'actionColor': [.2, .7, .9, 1],
            'activeColor': [1, 1, 1, 1],
            'inactiveColor': [1, 1, 1, 0.5],
            'redColor': [1, 0, 0, 0.5],
            'greenColor': [0, 1, 0, 0.5],
            'backupsToKeep': 10,
            'maxBackupAge': 1,
            'showSections': 'maybe',
        }
        try:
            with open(dataDir + '/settings.json') as fd:
                    settings = json.load(fd)
                    for key in defaultSettings:
                        if not key in settings:
                            settings[key] = defaultSettings[key]
        except:
            settings = defaultSettings

        backups = sorted(glob(f'{dataDir}/Plocka-*.json'))
        cutoff = (datetime.now() - timedelta(days=settings['maxBackupAge'])).strftime("%Y%m%d%H%M%S")
        for backup in backups[:-settings['backupsToKeep']]:
            if backup < f'{dataDir}/Plocka-{cutoff}.json':
                print('deleting backup file ' + backup)
                os.remove(backup)

        def hide(widget):
            if widget.height:
                widget.restore = widget.height
            widget.height = 0
            widget.opacity = 0
            widget.disabled = True

        def unhide(widget):
            if widget.disabled:
                widget.height = widget.restore
                widget.opacity = 1
                widget.disabled = False

        def checkSection(stack, current):
            for item in stack.children[::-1]:
                if item.type == 'section':
                    section = item
                if item == current:
                    break
            index = stack.children.index(section)
            for item in stack.children[index-1::-1]:
                if item.type == 'item' and item.check.state == 'normal':
                    return
                if item.type == 'section':
                    break
            hide(section)

        self.writeDeferred = False
        def writeFile(dt):
            if dt and not self.writeDeferred:
                return
            self.writeDeferred = False
            activeList = []
            for item in stack.children[::-1]:
                if item.type == 'item':
                    entry = {
                        "item": item.text,
                        "done": item.check.state == 'down'
                    }
                    section["items"].append(entry)
                elif item.type == 'section':
                    section = {
                        "section": item.origText,
                        "items": []
                    }
                    activeList.append(section)
            shoppingList['lists'][shoppingList['active']]['name'] = title.text
            shoppingList['lists'][shoppingList['active']]['list'] = activeList

            now = datetime.now().strftime("%Y%m%d%H%M%S")
            if os.path.exists(f'{dataDir}/Plocka.json'):
                os.rename(f'{dataDir}/Plocka.json', f'{dataDir}/Plocka-{now}.json')
            with open(f'{dataDir}/Plocka.json', 'w', encoding='utf8') as fd:
                json.dump(shoppingList, fd, indent=2, ensure_ascii=False)
            saveBtn.color = settings['greenColor']

        def undo(instance):
            global shoppingList
            try:
                last = sorted(glob(f'{dataDir}/Plocka-*.json'))[-1]
                os.rename(last, f'{dataDir}/Plocka.json')
                with open(dataDir + '/Plocka.json') as fd:
                        shoppingList = json.load(fd)
                populate()
                hideUnHide(hideBtn)
            except: pass

        def toggle(instance):
            if instance.check.state == 'down':
                instance.background_color = settings['itemColor']
                instance.color = settings['activeColor']
                instance.check.state = 'normal'
            else:
                instance.background_color = settings['doneColor']
                instance.color = settings['inactiveColor']
                instance.check.state = 'down'

            if not self.writeDeferred:
                self.writeDeferred = True
                saveBtn.color = settings['actionColor']
                Clock.schedule_once(writeFile, 1)

            if hideBtn.state == 'down' and instance.check.state == 'down':
                hide(instance.check)
                hide(instance)
                checkSection(stack, instance)

        def hideUnHide(instance):
            if hideBtn.state != "down" and not searchInput.text:
                for item in stack.children[:]:
                    unhide(item)

            elif searchInput.text == searchInput.text.upper() and searchInput.text != searchInput.text.lower():
                activeSection = False
                for item in stack.children[::-1]:
                    if item.type == 'section':
                        if re.search(searchInput.text, item.text):
                            activeSection = True
                        else:
                            activeSection = False
                    if activeSection and (
                            hideBtn.state != 'down' or
                            item.type != 'item' and item.type != 'check' or
                            hideBtn.state == 'down' and item.type == 'check' and item.state != 'down' or
                            hideBtn.state == 'down' and item.type == 'item' and item.check.state != 'down'
                    ):
                        unhide(item)
                    else:
                        hide(item)

            else:
                hasChildren = False
                regexp = searchInput.text if searchInput.text else '.'
                for item in stack.children[:]:
                    if item.type == 'item':
                        if hideBtn.state == "down" and item.check.state == 'down' or not re.search(regexp, item.text, re.IGNORECASE):
                            hide(item.check)
                            hide(item)
                        else:
                            unhide(item.check)
                            unhide(item)
                            hasChildren = True
                    elif item.type == 'section':
                        if hasChildren and settings['showSections'] == 'always':
                            unhide(item)
                            hasChildren = False
                        else:
                            hide(item)

        def crossCheck(instance):
            toggle(instance.label)

        def edit(instance):
            entry = TextInput(
                text = instance.text,
                size_hint = (0.5, None),
                height = settings['itemSize'],
                multiline = False,
                on_text_validate = lambda w: updateItem(w),
            )
            if instance.type == 'section':
                entry.text = instance.origText
            relative = ImageButton(
                source = 'data/left.png' if instance.type == 'item' else 'data/right.png',
                color_normal = [1, 1, 1, .7],
                height = settings['itemSize'],
                size_hint = (0.1, None),
                on_release = lambda w: updateItem(entry),
            )
            before = ImageButton(
                source = 'data/up.png',
                color_normal = [1, 1, 1, .7],
                height = settings['itemSize'],
                size_hint = (0.1, None),
                on_release = lambda w: updateItem(entry),
            )
            replace = ImageButton(
                source = 'data/ok.png',
                color_normal = [0, .5, 0, 1],
                height = settings['itemSize'],
                size_hint = (0.1, None),
                on_release = lambda w: updateItem(entry),
            )
            after = ImageButton(
                source = 'data/down.png',
                color_normal = [1, 1, 1, .7],
                height = settings['itemSize'],
                size_hint = (0.1, None),
                on_release = lambda w: updateItem(entry),
            )
            delete = ImageButton(
                source = 'data/delete.png',
                color_normal = [.5, 0, 0, 1],
                height = settings['itemSize'],
                size_hint = (0.1, None),
                on_release = lambda w: updateItem(entry),
            )
            entry.orig = instance
            entry.relative = relative
            entry.before = before
            entry.replace = replace
            entry.after = after
            entry.delete = delete

            entry.type = 'entry'
            relative.type = 'relative'
            before.type = 'before'
            replace.type = 'replace'
            after.type = 'after'
            delete.type = 'delete'

            hide(instance)
            if instance.type == 'item':
                hide(instance.check)
            index = stack.children.index(instance)
            stack.add_widget(delete, index)
            stack.add_widget(entry, index)
            stack.add_widget(relative, index)
            stack.add_widget(before, index)
            stack.add_widget(replace, index)
            stack.add_widget(after, index)
            entry.focused = True

        def updateItem(entry):
            todo = 'replace'
            if entry.delete.state == 'down':
                todo = 'delete'
            elif entry.before.state == 'down':
                todo = 'before'
            elif entry.after.state == 'down':
                todo = 'after'
            elif entry.relative.state == 'down':
                if entry.orig.type == 'section':
                    todo = 'item'
                else:
                    todo = 'section'

            orig = entry.orig
            text = entry.text

            stack.remove_widget(entry.relative)
            stack.remove_widget(entry.before)
            stack.remove_widget(entry.replace)
            stack.remove_widget(entry.after)
            stack.remove_widget(entry.delete)
            stack.remove_widget(entry)

            if todo == 'delete':
                stack.remove_widget(orig)
                if orig.type == 'item':
                    stack.remove_widget(orig.check)
            else:
                unhide(orig)
                if orig.type == 'item':
                    unhide(orig.check)
                if todo == 'replace':
                    if orig.type == 'section':
                        orig.origText = text
                        orig.text = text.upper()
                    else:
                        orig.text = text
                else:
                    if orig.type == 'section' and todo != 'item' or todo == 'section':
                        label = sectionButton(text)
                    else:
                        label = itemButtonPair(text, False)

                    index = stack.children.index(orig)
                    if todo == 'before' or todo == 'section':
                        index += 1
                    if orig.type == 'item':
                        if todo == 'before' or todo == 'section':
                            index += 1
                    if label.type == 'item':
                        stack.add_widget(label.check, index)
                    stack.add_widget(label, index)

            writeFile(0)

        self.searchDeferred = False
        def doSearch(text, undo):
            if not self.searchDeferred:
                self.searchDeferred = True
                Clock.schedule_once(filterOut, 1)
            return text

        def filterOut(dt):
            self.searchDeferred = False
            hideUnHide(hideBtn)

        def setBookmark():
            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            os.makedirs(f'{dataDir}/bookmarks', exist_ok=True)
            print(f"set bookmark '{dataDir}/bookmarks/{now}.json'")
            shutil.copy(f'{dataDir}/Plocka.json', f'{dataDir}/bookmarks/{now}.json')

        bookmark = ''
        def getBookmark():
            popup = Popup(
                title = "Bookmarks",
                content = BookmarkList(
                    dataDir = dataDir,
                    settings = settings,
                    orientation = 'vertical',
                ),
                size_hint = (0.9, 0.9),
            )
            popup.bind(on_pre_dismiss = useBookmark)
            popup.open()

        def useBookmark(w):
            global shoppingList
            bookmark = w.content.chosen
            if not bookmark:
                print('no bookmark chosen')
                return
            writeFile(0)
            shutil.copy(f'{dataDir}/bookmarks/{bookmark}.json', f'{dataDir}/Plocka.json')
            with open(f'{dataDir}/Plocka.json') as fd:
                    shoppingList = json.load(fd)
            populate()

        def selectList(w):
            global shoppingList

            dropdown = DropDown(
                on_select = lambda instance, selected: setActive(selected),
            )
            index = -1
            for item in shoppingList['lists']:
                index += 1
                if index == shoppingList['active']:
                    continue
                btn = Button(
                    text = item['name'],
                    size_hint_y = None,
                    background_color = settings['sectionColor'],
                    height=settings['itemSize'],
                )
                btn.index = index
                btn.bind(on_release=lambda btn: dropdown.select(btn.index))
                dropdown.add_widget(btn)

            about = Button(
                text = "About Plocka",
                size_hint_y = None,
                background_color = settings['sectionColor'],
                height=settings['itemSize'],
            )
            about.bind(on_release=lambda about: dropdown.select(-1))
            dropdown.add_widget(about)

            dropdown.open(w)

        def setActive(selected):
            if selected > -1:
                global shoppingList
                shoppingList['active'] = selected
                populate()
                writeFile(0)
            else:

                with open(scriptDir + '/ABOUT.rst') as fd:
                    about = fd.read()

                with open(scriptDir + '/LICENSE') as fd:
                    license = fd.read()

                aboutText = RstDocument(
                    text = about + '\n\nLicense\n-------\n\n' + license,
                )
                popup = Popup(
                    title = "Plocka " + __version__,
                    content = aboutText,
                )
                popup.open()

        def editList(w):
            buttonBox = BoxLayout()
            top.add_widget(buttonBox)
            delete = ImageButton(
                source = 'data/delete.png',
                color_normal = [.5, 0, 0, 1],
                size_hint_x = None,
                width = settings['headerSize'],
                on_release = lambda w: deleteList(w),
            )
            buttonBox.add_widget(delete)
            entry = TextInput(
                text = w.text,
                height = settings['headerSize'],
                multiline = False,
                on_text_validate = lambda w: setListName(w),
            )
            buttonBox.add_widget(entry)
            saveBtn = ImageButton(
                source = "data/ok.png",
                color_normal = settings['greenColor'],
                size_hint_x = None,
                width = settings['headerSize'],
                on_release = lambda x: setListName(entry),
            )
            buttonBox.add_widget(saveBtn)
            copy = ImageButton(
                source = 'data/copy.png',
                color_normal = [1, 1, 1, .7],
                size_hint_x = None,
                width = settings['headerSize'],
                on_release = lambda w: copyList(w),
            )
            buttonBox.add_widget(copy)
            new = ImageButton(
                source = 'data/new.png',
                color_normal = settings['greenColor'],
                size_hint_x = None,
                width = settings['headerSize'],
                on_release = lambda w: createList(entry),
            )
            buttonBox.add_widget(new)

            top.remove_widget(title)
            top.remove_widget(searchBtn)
            entry.focused = True

        def closeEditor(w):
            top.add_widget(title)
            top.add_widget(searchBtn)
            top.remove_widget(w.parent)

        def setListName(w):
            title.text = w.text
            closeEditor(w)
            writeFile(0)

        def createList(w):
            global shoppingList
            new = {
                'name': 'New list',
                'list': [{
                    'section': 'Section',
                    'items': []
                }]}
            at = shoppingList['active'] + 1
            shoppingList['lists'].insert(at, new)
            setActive(at)
            closeEditor(w)

        def copyList(w):
            global shoppingList
            at = shoppingList['active']
            new = json.loads(json.dumps(shoppingList['lists'][at]))
            new['name'] += ' 2'
            at += 1
            shoppingList['lists'].insert(at, new)
            setActive(at)
            closeEditor(w)

        def deleteList(w):
            at = shoppingList['active']
            del(shoppingList['lists'][at])
            if at >= len(shoppingList['lists']):
                at = at - 1
            setActive(at)
            closeEditor(w)

        # Widgets

        def sectionButton(text):
            label = LongpressButton(
                text = text.upper(),
                font_size = settings['sectionTextSize'],
                height = settings['sectionSize'],
                background_color = settings['sectionColor'],
                size_hint = (1, None),
                on_long_press = lambda w: edit(w),
            )
            label.origText = text
            label.type = 'section'
            return label

        def itemButtonPair(text, done):
            label = LongpressButton(
                text = text,
                height = settings['itemSize'],
                background_color = settings['itemColor'],
                size_hint = (0.95, None),
                on_short_press = lambda w: toggle(w),
                on_long_press = lambda w: edit(w),
            )
            label.type = 'item'
            check = CheckBox(
                height = settings['itemSize'],
                size_hint = (0.05, None),
                on_release = lambda w: crossCheck(w),
            )
            if done:
                  label.background_color = settings['doneColor']
                  label.color = settings['inactiveColor']
                  check.state = 'down'
            check.type = 'check'
            check.label = label
            label.check = check
            return label

        def populate():
            global shoppingList
            if not 'lists' in shoppingList:
                shoppingList = {
                    'lists': [
                      {
                        'name': 'Plocka',
                        'list': shoppingList
                      }
                    ]
                }
            if not 'active' in shoppingList:
                shoppingList['active'] = 0
            title.text = shoppingList['lists'][shoppingList['active']]['name']
            stack.clear_widgets()
            for section in shoppingList['lists'][shoppingList['active']]['list']:
                if settings['showSections'] != 'never':
                    sectionLabel = sectionButton(section['section'])
                    stack.add_widget(sectionLabel)
                for item in section['items']:
                    label = itemButtonPair(item['item'], item['done'])
                    stack.add_widget(label.check)
                    stack.add_widget(label)

        def toggleSearch(widget):
            if searchInput.disabled:
                top.add_widget(searchInput,1)
                searchInput.disabled = False
                searchInput.focused = True
            else:
                searchInput.text = ''
                searchInput.disabled = True
                top.remove_widget(searchInput)
                hideUnHide(hideBtn)

        # MAIN

        top = BoxLayout(
            size_hint=(1, None),
            height = settings['headerSize'],
        )
        self.add_widget(top)

        title = LongpressButton(
            text = 'Unknown',
            background_color = settings['sectionColor'],
            on_short_press = selectList,
            on_long_press = editList,
        )
        top.add_widget(title)

        searchBtn = ImageButton(
            source = 'data/search.png',
            width = settings['headerSize'],
            color_normal = [1, 1, 1, .6],
            on_release = toggleSearch,
            size_hint_x = None,
        )
        top.add_widget(searchBtn)
        searchInput = TextInput(
            disabled = True,
            multiline = False,
            input_filter = doSearch,
            on_text_validate = lambda w: hideUnHide(hideBtn),
        )

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

        populate()

        buttons = BoxLayout(
            size_hint=(1, None),
            height = settings['headerSize'],
        )
        self.add_widget(buttons)
        saveBtn = ImageButton(
            source = "data/ok.png",
            color_normal = settings['greenColor'],
            on_release = lambda x: writeFile(0),
        )
        buttons.add_widget(saveBtn)

        hideBtn = ToggleImageButton(
            image_down = "data/show.png",
            image_normal = "data/hide.png",
            color_down = [1, 1, 1, .9],
            color_normal = [1, 1, 1, .6],
            on_release = hideUnHide,
        )
        buttons.add_widget(hideBtn)

        undoBtn = ImageButton(
            source = 'data/undo.png',
            color_normal = settings['redColor'],
            on_release = undo,
        )
        buttons.add_widget(undoBtn)

        bookmarkBtn = LongpressImageButton(
            source = 'data/bookmark.png',
            color_normal = settings['greenColor'],
            on_short_press = lambda w: setBookmark(),
            on_long_press = lambda w: getBookmark(),
        )
        buttons.add_widget(bookmarkBtn)

class Plocka(App):

    def build(self):
        return CheckList(orientation = 'vertical')

if __name__ == '__main__':
    Plocka().run()

