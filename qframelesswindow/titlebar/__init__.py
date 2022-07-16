# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QHBoxLayout, QWidget

if sys.platform == "win32":
    import win32con
    from win32api import SendMessage
    from win32gui import ReleaseCapture
elif sys.platform == "darwin":
    from ..utils.mac_utils import MacMoveResize
else:
    from ..utils.linux_utils import LinuxMoveResize

from .title_bar_buttons import CloseButton, MaximizeButton, MinimizeButton


class TitleBarBase(QWidget):
    """ Title bar base class """

    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self.hBoxLayout = QHBoxLayout(self)

        self.resize(200, 32)
        self.setFixedHeight(32)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignRight)

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.LeftButton:
            return

        self.__toggleMaxState()

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        return 0 < pos.x() < self.width() - 46 * 3


class WindowsTitleBar(TitleBarBase):
    """ Title bar for Windows system """

    def mouseMoveEvent(self, event):
        if not self._isDragRegion(event.pos()):
            return

        ReleaseCapture()
        SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                    win32con.SC_MOVE | win32con.HTCAPTION, 0)
        event.ignore()


class LinuxTitleBar(TitleBarBase):
    """ Title bar for Unix system """

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self._isDragRegion(event.pos()):
            return

        LinuxMoveResize.startSystemMove(self.window(), event.globalPos())


class MacTitleBar(TitleBarBase):
    """ Title bar for Mac OS """

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self._isDragRegion(event.pos()):
            return

        MacMoveResize.startSystemMove(self.window(), event.globalPos())


if sys.platform == "win32":
    TitleBar = WindowsTitleBar
elif sys.platform == "darwin":
    TitleBar = MacTitleBar
else:
    TitleBar = LinuxTitleBar
