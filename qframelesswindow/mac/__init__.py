# coding:utf-8
import Cocoa
import objc
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QWidget, QMainWindow, QDialog

from ..titlebar import TitleBar
from .window_effect import MacWindowEffect


class MacFramelessWindowBase:
    """ Frameless window base class for mac """

    def __init__(self, *args, **kwargs):
        pass

    def _initFrameless(self):
        self.windowEffect = MacWindowEffect(self)
        # must enable acrylic effect before creating title bar
        if isinstance(self, AcrylicWindow):
            self.windowEffect.setAcrylicEffect(self.winId())

        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        view = objc.objc_object(c_void_p=self.winId().__int__())
        self.__nsWindow = view.window()

        # hide system title bar
        self._hideSystemTitleBar()

        self.resize(500, 500)
        self.titleBar.raise_()

    def setTitleBar(self, titleBar):
        """ set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def resizeEvent(self, e):
        self.titleBar.resize(self.width(), self.titleBar.height())

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self._hideSystemTitleBar()

    def _hideSystemTitleBar(self):
        # extend view to title bar region
        self.__nsWindow.setStyleMask_(
            self.__nsWindow.styleMask() | Cocoa.NSFullSizeContentViewWindowMask)
        self.__nsWindow.setTitlebarAppearsTransparent_(True)

        # disable the moving behavior of system
        self.__nsWindow.setMovableByWindowBackground_(False)
        self.__nsWindow.setMovable_(False)

        # hide title bar buttons and title
        self.__nsWindow.setShowsToolbarButton_(False)
        self.__nsWindow.setTitleVisibility_(Cocoa.NSWindowTitleHidden)
        self.__nsWindow.standardWindowButton_(Cocoa.NSWindowCloseButton).setHidden_(True)
        self.__nsWindow.standardWindowButton_(Cocoa.NSWindowZoomButton).setHidden_(True)
        self.__nsWindow.standardWindowButton_(Cocoa.NSWindowMiniaturizeButton).setHidden_(True)


class MacFramelessWindow(QWidget, MacFramelessWindowBase):
    """ Frameless window for Linux system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()

    def resizeEvent(self, e):
        MacFramelessWindowBase.resizeEvent(self, e)

    def changeEvent(self, e):
        MacFramelessWindowBase.changeEvent(self, e)

    def paintEvent(self, e):
        QWidget.paintEvent(self, e)
        self._hideSystemTitleBar()


class AcrylicWindow(MacFramelessWindow):
    """ A frameless window with acrylic effect """

    def _initFrameless(self):
        super()._initFrameless()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.windowEffect.setAcrylicEffect(self.winId())
        self.setStyleSheet("background: transparent")


class MacFramelessMainWindow(QMainWindow, MacFramelessWindowBase):
    """ Frameless window for Linux system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()

    def resizeEvent(self, e):
        QMainWindow.resizeEvent(self, e)
        MacFramelessWindowBase.resizeEvent(self, e)

    def changeEvent(self, e):
        MacFramelessWindowBase.changeEvent(self, e)

    def paintEvent(self, e):
        QMainWindow.paintEvent(self, e)
        self._hideSystemTitleBar()


class MacFramelessDialog(QDialog, MacFramelessWindowBase):
    """ Frameless window for Linux system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)

    def resizeEvent(self, e):
        MacFramelessWindowBase.resizeEvent(self, e)

    def changeEvent(self, e):
        MacFramelessWindowBase.changeEvent(self, e)

    def paintEvent(self, e):
        QDialog.paintEvent(self, e)
        self._hideSystemTitleBar()
