# Checker

A simple cross platform checklist app.

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
buildozer init

find . -perm 0444 | xargs -r chmod u+w
buildozer android debug deploy run
```

### Install an already built app with ADB
```
adb install bin/checker-0.1-armeabi-v7a-debug.apk
```

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

The data file is named `Checker.json` and should be in `$HOME.config/Checker/` on Linux
and `/sdcard/Android/data/se.jonaseel.checker/files` on Android. There may also be a
`settings.json` in the same directory.

### License

This app is released under a BSD License; see the `LICENSE` file.
