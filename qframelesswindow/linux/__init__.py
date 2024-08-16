# coding:utf-8
from PySide6.QtCore import QCoreApplication, QEvent, Qt, QSize, QRect
from PySide6.QtWidgets import QWidget, QMainWindow, QDialog

from ..titlebar import TitleBar
from ..utils.linux_utils import LinuxMoveResize
from .window_effect import LinuxWindowEffect


class LinuxFramelessWindowBase:
    """ Frameless window base class for Linux system """

    BORDER_WIDTH = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._isSystemButtonVisible = False

    def _initFrameless(self):
        self.windowEffect = LinuxWindowEffect(self)
        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        self.updateFrameless()
        QCoreApplication.instance().installEventFilter(self)

        self.titleBar.raise_()
        self.resize(500, 500)

    def updateFrameless(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def resizeEvent(self, e):
        self.titleBar.resize(self.width(), self.titleBar.height())

    def setTitleBar(self, titleBar):
        """ set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar.hide()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def isSystemButtonVisible(self):
        """ Returns whether the system title bar button is visible """
        return self._isSystemButtonVisible

    def setSystemTitleBarButtonVisible(self, isVisible):
        """ set the visibility of system title bar button, only works for macOS """
        pass

    def systemTitleBarRect(self, size: QSize) -> QRect:
        """ Returns the system title bar rect, only works for macOS

        Parameters
        ----------
        size: QSize
            original system title bar rect
        """
        return QRect(0, 0, size.width(), size.height())

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPos() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width()-self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height()-self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        # change cursor
        if et == QEvent.MouseMove and self.windowState() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        elif obj in (self, self.titleBar) and et == QEvent.MouseButtonPress and edges:
            LinuxMoveResize.starSystemResize(self, event.globalPos(), edges)

        return False


class LinuxFramelessWindow(LinuxFramelessWindowBase, QWidget):
    """ Frameless window for Linux system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()


class LinuxFramelessMainWindow(LinuxFramelessWindowBase, QMainWindow):
    """ Frameless main window for Linux system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()


class LinuxFramelessDialog(LinuxFramelessWindowBase, QDialog):
    """ Frameless dialog for Windows system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
