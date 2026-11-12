# coding:utf-8
from PyQt5.QtCore import QEvent, Qt, QSize, QRect
from PyQt5.QtWidgets import QWidget

from ..titlebar import TitleBar
from .window_effect import LinuxWindowEffect


EDGE_CURSORS = {
    Qt.LeftEdge | Qt.TopEdge: Qt.SizeFDiagCursor,
    Qt.RightEdge | Qt.BottomEdge: Qt.SizeFDiagCursor,
    Qt.RightEdge | Qt.TopEdge: Qt.SizeBDiagCursor,
    Qt.LeftEdge | Qt.BottomEdge: Qt.SizeBDiagCursor,
    Qt.TopEdge: Qt.SizeVerCursor,
    Qt.BottomEdge: Qt.SizeVerCursor,
    Qt.LeftEdge: Qt.SizeHorCursor,
    Qt.RightEdge: Qt.SizeHorCursor,
}


class LinuxFramelessWindow(QWidget):
    """ Frameless window for Linux system """

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.windowEffect = LinuxWindowEffect(self)
        self.titleBar = TitleBar(self)
        self._isSystemButtonVisible = False
        self._isResizeEnabled = True

        self.updateFrameless()

        # Wayland does not expose the window position
        self.winId()
        self.windowHandle().installEventFilter(self)

        self.titleBar.raise_()
        self.resize(500, 500)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def updateFrameless(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def refreshBackgroundBlurEffect(self):
        """ Refresh background blur effect """
        pass

    def setStayOnTop(self, isTop: bool):
        """ set the stay on top status """
        if isTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

        self.updateFrameless()
        self.show()

    def toggleStayOnTop(self):
        """ toggle the stay on top status """
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setStayOnTop(False)
        else:
            self.setStayOnTop(True)

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
        if obj is not self.windowHandle() or et not in (QEvent.MouseButtonPress, QEvent.MouseMove):
            return super().eventFilter(obj, event)

        if not self._isResizeEnabled or self.isMaximized() or self.isFullScreen():
            return super().eventFilter(obj, event)

        edges = Qt.Edges()
        pos = event.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        elif pos.x() >= self.width() - self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        elif pos.y() >= self.height() - self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        if et == QEvent.MouseMove:
            self.setCursor(EDGE_CURSORS.get(edges, Qt.ArrowCursor))
        elif edges and event.button() == Qt.LeftButton:
            # fix issue #160
            return obj.startSystemResize(edges)

        return super().eventFilter(obj, event)
