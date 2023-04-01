# README

[![Stability](https://img.shields.io/badge/Stability-WIP-lightgrey.svg)](https://github.com/MuSmile/DearEditor)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1)
[![Documentation](https://img.shields.io/badge/Docs-Click_Me-brightgreen.svg)](https://musmile.github.io/DearDoc/)

> Your next Unity is not a Unity...

DearEditor is a PySide6 based runtime-free game engine editor.

DearEditor aims to create an open and unite editor solution for all engine runtime(especially in-house engines).


## Screenshots
![screenshot](docs/_static/screenshots/p1.png)
![screenshot](docs/_static/screenshots/p2.png)


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

## One more thing...
If this project help you reduce time to develop or if you just like it, you can buy me a cup of coffee ☕😉.

Donate with Paypal|Donate with Alipay|Donate with WeChat
:-----------------|:-----------------|:-----------------
[![donate_paypal](docs/_static/donate/donate_paypal.png)](https://paypal.me/kakikodesu)|[![donate_alipay](docs/_static/donate/donate_alipay.png)](https://raw.githubusercontent.com/MuSmile/DearEditor/master/docs/_static/donate/qrcode_alipay.jpeg)|[![donate_wechatpay](docs/_static/donate/donate_wechatpay.png)](https://raw.githubusercontent.com/MuSmile/DearEditor/master/docs/_static/donate/qrcode_wechatpay.jpeg)
