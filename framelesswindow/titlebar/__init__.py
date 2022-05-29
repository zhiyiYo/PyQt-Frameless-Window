# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget

if sys.platform == "win32":
    from win32.lib import win32con
    from win32.win32api import SendMessage
    from win32.win32gui import ReleaseCapture
else:
    from ..utils.linux_utils import LinuxMoveResize

from .title_bar_buttons import CloseButton, MaximizeButton, MinimizeButton


class TitleBar(QWidget):

    def __new__(cls, *args, **kwargs):
        cls = WindowsTitleBar if sys.platform == "win32" else UnixTitleBar
        return super().__new__(cls, *args, **kwargs)

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
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignRight)

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.LeftButton:
            return

        self.__toggleMaxState()

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
            # change the icon of maxBtn
            self.maxBtn.setMaxState(False)
        else:
            self.window().showMaximized()
            self.maxBtn.setMaxState(True)

    def _isDragRegion(self, pos) -> bool:
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        right = self.width() - 46 * 3 if self.minBtn.isVisible() else self.width() - 46
        return 0 < pos.x() < right


class WindowsTitleBar(TitleBar):
    """ Title bar for Windows system """

    def mousePressEvent(self, event):
        """ Move the window """
        if not self._isDragRegion(event.pos()):
            return

        ReleaseCapture()
        SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                    win32con.SC_MOVE + win32con.HTCAPTION, 0)
        event.ignore()


class UnixTitleBar(TitleBar):
    """ Title bar for Unix system """

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self._isDragRegion(event.pos()):
            return

        pos = event.globalPos()
        LinuxMoveResize.startSystemMove(self.window(), pos)
