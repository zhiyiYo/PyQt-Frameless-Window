"""
PySide6-Frameless-Window
========================
A cross-platform frameless window based on pyside6, support Win32, Linux and macOS.

Documentation is available in the docstrings and
online at https://pyqt-frameless-window.readthedocs.io.

Examples are available at https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6/examples.

:copyright: (c) 2021 by zhiyiYo.
:license: LGPLv3, see LICENSE for more details.
"""

__version__ = "0.0.5"

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMainWindow

from .titlebar import TitleBar, TitleBarButton, SvgTitleBarButton, StandardTitleBar

if sys.platform == "win32":
    from .windows import AcrylicWindow as AcrylicWindowBase
    from .windows import WindowsFramelessWindow as FramelessWindowBase
    from .windows import WindowsWindowEffect as WindowEffect
elif sys.platform == "darwin":
    from .mac import AcrylicWindow as AcrylicWindowBase
    from .mac import MacFramelessWindow as FramelessWindowBase
    from .mac import MacWindowEffect as WindowEffect
else:
    from .linux import LinuxFramelessWindow as FramelessWindowBase
    from .linux import LinuxWindowEffect as WindowEffect

    AcrylicWindowBase = FramelessWindowBase


class FramelessWindow(FramelessWindowBase):
    """ Frameless window """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()


class FramelessDialog(QDialog, FramelessWindowBase):
    """ Frameless dialog """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)

    def resizeEvent(self, e):
        self.titleBar.resize(self.width(), self.titleBar.height())


class FramelessMainWindow(QMainWindow, FramelessWindowBase):
    """ Frameless main window """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()


class AcrylicWindow(AcrylicWindowBase):
    """ Acrylic window """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()