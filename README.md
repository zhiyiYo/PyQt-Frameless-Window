<p align="center">
  <img width="15%" align="center" src="https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/logo.png" alt="logo">
</p>
  <h1 align="center">
  PySide6-Frameless-Window
</h1>
<p align="center">
  A cross-platform frameless window based on PySide6
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820" alt="Platform Win32 | Linux | macOS"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://static.pepy.tech/personalized-badge/pysidesix_frameless_window?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Download"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-LGPLv3-blue?color=#4ec820" alt="LGPLv3"/>
  </a>
</p>

![Cover](https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/cover.jpg)

## Features
* Moving
* Stretching
* Window shadow
* Window animation
* Win11 snap layout
* Win10 acrylic blur
* Win11 mica blur
* Win7 Aero blur
* MacOS blur

## Install
To install use pip:
```shell
pip install PySideSix-Frameless-Window
```
Or clone the repo:
```shell
git clone -b PySide6 https://github.com/zhiyiYo/PyQt-Frameless-Window.git
python setup.py install
```

## Requirements

| Platform | Requirement |
| :------: | :---------: |
|  Win32   |   pywin32   |
|  MacOS   |   pyobjc    |


## Usage
To use the frameless window, you only need to inherit `FramelessWindow` or `FramelessMainWindow`. Here is a minimal example:
```python
import sys

from PySide6.QtWidgets import QApplication
from qframelesswindow import FramelessWindow


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("PySide6-Frameless-Window")
        self.titleBar.raise_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    app.exec()
```
For more complex requirements, see [demo.py](https://github.com/zhiyiYo/PyQt-Frameless-Window/blob/PySide6/examples/demo.py) and [main_window.py](https://github.com/zhiyiYo/PyQt-Frameless-Window/blob/PySide6/examples/main_window.py).

## Examples
* Normal frameless window
![Normal Frameless Window](https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/normal_frameless_window.gif)
* Acrylic frameless window
![Acrylic Frameless Window](https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/acrylic_window.jpg)


## Document
Want to know more about PySide6-Frameless-Window? Please read the [help document](https://pyqt-frameless-window.readthedocs.io/) 👈

## Notes
1. `FramelessWindow` provides a default custom title bar. If you don't like it, just rewrite it as [demo.py](https://github.com/zhiyiYo/PyQt-Frameless-Window/blob/PySide6/examples/demo.py) does.

2. Moving the acrylic window on Win10 may get stuck. At present, there is no good solution. Maybe you can disable the acrylic effect when moving the window, but I haven't done this in the source code.
3. Snap layout is not enabled by default. See [#56](https://github.com/zhiyiYo/PyQt-Frameless-Window/issues/56) to learn how to enable it.

4. If you encounter this problem on Windows:
   > ImportError: DLL load failed while importing win32api

   see my answer on [stackoverflow](https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api/72488468#72488468) or my [blog](https://www.cnblogs.com/zhiyiYo/p/16340429.html) for the solution.

5. If you are using PySide2, PyQt5 or PyQt6, you can download the code in [PySide2](https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/Pyside2), [PyQt5](https://github.com/zhiyiYo/PyQt-Frameless-Window) or [PyQt6](https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PyQt6) branch.


## See Also
Here are some projects that use PyQt-Frameless-Window:
* [**zhiyiYo/Groove**: A cross-platform music player based on PyQt5](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: A gobang robot based on reinforcement learning](https://github.com/zhiyiYo/Alpha-Gobang-Zero)
* [**zhiyiYo/PyQt-Fluent-Widgets**: A fluent design widgets library based on PyQt5](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)
* [**zhiyiYo/QMaterialWidgets**: A material design widgets library based on PySide](https://github.com/zhiyiYo/QMaterialWidgets)

## Reference
* [**wangwenx190/framelesshelper**: Frameless windows for Qt Widgets and Qt Quick applications. Support Win32, X11, Wayland and macOS](https://github.com/wangwenx190/framelesshelper)
* [**libxcb**: Basic Graphics Programming With The XCB Library](https://www.x.org/releases/X11R7.5/doc/libxcb/tutorial)

## License
PySide6-Frameless-Window is licensed under [LGPLv3](./LICENSE).

Copyright © 2021 by zhiyiYo.
