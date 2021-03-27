### Relevant commands

```
git clone https://github.com/kivy/buildozer.git
cd buildozer
python setup.py install
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

cd -
buildozer init

find . -perm 0444 | xargs -r chmod u+w
buildozer android debug deploy run

adb install bin/checker-0.1-armeabi-v7a-debug.apk
```

### Data format

```
[
  {"Section 1": [
    {"item": "Item 1", "done": true},
    {"item": "Item 2", "done": true},
    {"item": "Item 3", "done": true}
  ]},
  {"Section 2": [
    {"item": "Item 1", "done": true},
    {"item": "Item 2", "done": true},
    {"item": "Item 3", "done": true},
    {"item": "Item 4", "done": true}
  ]},
  {"Section 3": [
    {"item": "Item 1", "done": true},
    {"item": "Item 2", "done": true},
    {"item": "Item 3", "done": true}
  ]}
]
```
