# Checker

A simple cross platform checklist app.

### Why

In spite of trying out a number of existing apps, I've failed to find one that works the way I
would like and that isn't too buggy.

### Download and install prerequisites

```
git clone https://github.com/krakan/checker.git
cd checker
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
adb install bin/checker-0.1-armeabi-v7a-debug.apk
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

The data file is named `Checker.json` and should be in `$HOME/.config/Checker/` on Linux and
`/sdcard/Android/data/se.jonaseel.checker/files` on Android. There may also be a
`settings.json` in the same directory. The data file location on iOS needs to be decided.

### License

This app and the Kivy library are both released under the MIT License; see the `LICENSE` file.
