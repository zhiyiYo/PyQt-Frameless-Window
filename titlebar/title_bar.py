# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget
from win32.lib import win32con
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture

from .title_bar_buttons import MinimizeButton, MaximizeButton, CloseButton


class TitleBar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self.__initWidget()

    def __initWidget(self):
        """ initialize all widgets """
        self.resize(1360, 32)
        self.setFixedHeight(32)
        self.setAttribute(Qt.WA_StyledBackground)
        self.__setQss()

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

    def resizeEvent(self, e: QResizeEvent):
        """ Move the buttons """
        self.closeBtn.move(self.width() - 46, 0)
        self.maxBtn.move(self.width() - 2 * 46, 0)
        self.minBtn.move(self.width() - 3 * 46, 0)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        self.__toggleMaxState()

    def mousePressEvent(self, event):
        """ Move the window """
        if not self.__isPointInDragRegion(event.pos()):
            return

        ReleaseCapture()
        SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                    win32con.SC_MOVE + win32con.HTCAPTION, 0)
        event.ignore()

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
            # change the icon of maxBtn
            self.maxBtn.setMaxState(False)
        else:
            self.window().showMaximized()
            self.maxBtn.setMaxState(True)

    def __isPointInDragRegion(self, pos) -> bool:
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        right = self.width() - 46 * 3 if self.minBtn.isVisible() else self.width() - 46
        return (0 < pos.x() < right)

    def __setQss(self):
        """ 设置层叠样式 """
        with open('resource/qss/title_bar.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
