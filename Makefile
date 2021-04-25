help:
	@echo deploy build release install run

deploy:
	buildozer android debug deploy run

build:
	buildozer android debug

release:
	buildozer android release

install:
	adb install bin/plocka-$$(grep __version__ main.py | cut -d"'" -f2)-armeabi-v7a-debug.apk

run:
	python main.py
