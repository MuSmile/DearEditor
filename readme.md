# README

> Your next Unity is not a Unity...

DearEditor is a PySide6 based **WIP** runtime-free game engine editor.

The aim of DearEditor is to create an open and unite editor solution for all engine runtime(especially in-house engines).

## Screenshots
![screenshot](.support/pyside6_qtads/img/p1.png)
![screenshot](.support/pyside6_qtads/img/p2.png)


## Requirements
### 1. Install python >= 3.9.9
This project has only been developed and tested in python version 3.9.9.

Other compatible versions may be fine theoretically though...

Stick on this version could help to keep away from annoy issues.

### 2. Install required python packages
```bat
> pip install -r requirements.txt
```
or simply (need config project first)
```bat
> dear install
```

### 3. Additional requirements on MacOS
```bat
> pip install pyobjc-framework-Cocoa
```

## Config project
1. Add `<your-path>/DearEditor/bin` into environment variable `path`.
2. Find `<your-path>/DearEditor/bin/dear` file (`dear` for MacOS, and `dear.bat` for Windows).
3. Modify `idedir` and `pybin` path in dear file with your actual path.

## Enjoy and run
use ↓

```bat
> dear
```
to see welcome and usage info.

use ↓

```bat
> dear ide
```
to raise dear editor ide.

use ↓

```bat
> dear list
```
to check all available commands.
