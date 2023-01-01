import sys

from PyQt5.QtWidgets import QDialog, QMainWindow

from .titlebar import TitleBar

if sys.platform == "win32":
    from .windows import AcrylicWindow
    from .windows import WindowsFramelessWindow as FramelessWindow
    from .windows import WindowsWindowEffect as WindowEffect
elif sys.platform == "darwin":
    from .mac import AcrylicWindow
    from .mac import MacFramelessWindow as FramelessWindow
    from .mac import MacWindowEffect as WindowEffect
else:
    from .linux import LinuxFramelessWindow as FramelessWindow
    from .linux import LinuxWindowEffect as WindowEffect

    AcrylicWindow = FramelessWindow


class FramelessDialog(QDialog, FramelessWindow):
    """ Frameless dialog """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)


class FramelessMainWindow(QMainWindow, FramelessWindow):
    """ Frameless main window """

    def __init__(self, parent=None):
        super().__init__(parent)