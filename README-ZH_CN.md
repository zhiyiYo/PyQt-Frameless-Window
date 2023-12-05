<p align="center">
  <img width="15%" align="center" src="https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/logo.png" alt="logo">
</p>
<h1 align="center">
  PyQt-Frameless-Window
</h1>
<p align="center">
  一个基于PyQt5的跨平台无边框窗口
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820" alt="平台 Win32 | Linux | macOS"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://static.pepy.tech/personalized-badge/pyqt5-frameless-window?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="下载"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>
</p>

![封面](https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/cover.jpg)


## 特性
* 移动
* 调整大小
* 窗口阴影
* 窗口动画
* Win11 切片布局
* Win10 亚克力模糊
* Win11 云母模糊
* Win7 Aero 模糊
* MacOS 模糊

## 安装
使用 pip 安装:
```shell
pip install PyQt5-Frameless-Window
```
或克隆仓库:
```shell
git clone https://github.com/zhiyiYo/PyQt-Frameless-Window.git
python setup.py install
```

## 要求

| 平台 | 要求 |
| :------: | :---------: |
|  Win32   |   pywin32   |
|  Linux   |   xcffib    |
|  MacOS   |   pyobjc    |


## 用法
要使用无边框窗口，只需继承 `FramelessWindow` 或 `FramelessMainWindow`。以下是一个最简示例:
```python
import sys

from PyQt5.QtWidgets import QApplication
from qframelesswindow import FramelessWindow


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("PyQt-Frameless-Window")
        self.titleBar.raise_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())
```
对于更复杂的需求，请参阅 [demo.py](https://github.com/zhiyiYo/PyQt-Frameless-Window/blob/master/examples/demo.py) 和 [main_window.py](https://github.com/zhiyiYo/PyQt-Frameless-Window/blob/master/examples/main_window.py)。

## 示例
* 普通无边框窗口
![普通无边框窗口](https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/normal_frameless_window.gif)
* 亚克力无边框窗口
![亚克力无边框窗口](https://raw.githubusercontent.com/zhiyiYo/PyQt-Frameless-Window/master/screenshot/acrylic_window.jpg)


## 文档
想了解更多关于 PyQt-Frameless-Window 的信息吗？请阅读 [帮助文档](https://pyqt-frameless-window.readthedocs.io/) 👈


## 注意事项
1. `FramelessWindow` 提供了一个默认的自定义标题栏。如果不喜欢，只需像 [demo.py](https://github.com/zhiyiYo/PyQt-Frameless-Window/blob/master/examples/demo.py) 中那样重新编写它。

2. 在 Win10 上移动亚克力窗口可能会卡住。目前还没有很好的解决方案。也许在移动窗口时可以禁用亚克力效果，但我在源代码中还没有这样做。
3. 切片布局默认未启用。请查看[#56](https://github.com/zhiyiYo/PyQt-Frameless-Window/issues/56)以了解如何启用。

4. 如果在 Windows 上遇到此问题:
   > ImportError: DLL load failed while importing win32api

   可以查看我在 [stackoverflow](https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api/72488468#72488468) 上的回答或我的 [博客](https://www.cnblogs.com/zhiyiYo/p/16340429.html) 中的解决方案。

5. 如果使用 PySide2、PySide6 或 PyQt6，可以在 [PySide2](https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/Pyside2)、[PySide6](https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6) 或 [PyQt6](https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PyQt6) 分支中下载代码。

## 支持
如果这个项目对您有很大帮助，您想支持该项目的开发和维护，可以通过 [爱发电](https://afdian.net/a/zhiyiYo) 或 [ko-fi](https://ko-fi.com/zhiyiYo) 赞助我。非常感谢您的支持 🥰

## 参考
以下是一些使用 PyQt-Frameless-Window 的项目:
* [**zhiyiYo/Groove**: 基于 PyQt5 的跨平台音乐播放器](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: 基于强化学习的五子棋机器人](https://github.com/zhiyiYo/Alpha-Gobang-Zero)
* [**zhiyiYo/PyQt-Fluent-Widgets**: 基于 PyQt5 的流畅设计小部件库](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)
 * [**zhiyiYo/QMaterialWidgets**: 基于 PySide 的材料设计小部件库](https://github.com/zhiyiYo/QMaterialWidgets)

## 参考
 * [**wangwenx190/framelesshelper**: 为 Qt Widgets 和 Qt Quick 应用程序提供无边框窗口。支持 Win32、X11、Wayland 和 macOS](https://github.com/wangwenx190/framelesshelper)
 * [**libxcb**: 使用 XCB 库进行基本图形编程](https://www.x.org/releases/X11R7.5/doc/libxcb/tutorial)

## 许可证
PyQt-Frameless-Window 使用 [GPLv3](./LICENSE) 许可。

版权所有 © 2021 年 zhiyiYo。