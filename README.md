# Plocka

A simple cross platform checklist app.

### Why

In spite of trying out a number of existing apps, I've failed to find one that works the way I
would like and that isn't too buggy.

### Download and install prerequisites

```
git clone https://github.com/krakan/plocka.git
cd plocka
git clone https://github.com/kivy/buildozer.git
cd buildozer
python setup.py install
sudo apt install -y git zip unzip autoconf libtool pkg-config cmake \
    openjdk-8-jdk python3-pip \
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 libffi-dev libssl-dev
cd -
```

### Build for Android
```
buildozer android debug deploy run
```

#### Install an already built app with ADB
```
adb install bin/plocka-1.0-armeabi-v7a-debug.apk
```

### Build for iOS

This should work but hasn't been tested. See
https://kivy.org/doc/stable/guide/packaging-ios.html

### Data format

```
            [
              {"section": "Section 1", "items": [
                {"item": "Item 1", "done": false},
                {"item": "Item 2", "done": true},
                {"item": "Item 3", "done": true}
              ]},
              {"section": "Section 2", "items": [
                {"item": "Item 1", "done": true},
                {"item": "Item 2", "done": false},
                {"item": "Item 3", "done": false},
                {"item": "Item 4", "done": true}
              ]},
              {"section": "Section 3", "items": [
                {"item": "Item 1", "done": true},
                {"item": "Item 2", "done": true},
                {"item": "Item 3", "done": false}
              ]}
            ]
```

The data file is named `Plocka.json` and should be in `$HOME/.config/Plocka/` on Linux and
`/sdcard/Android/data/se.jonaseel.plocka/files` on Android. There may also be a
`settings.json` in the same directory. The data file location on iOS needs to be decided.

### License

This app, the Kivy library and the icons used are all released under the MIT License; see the
`LICENSE` file.
