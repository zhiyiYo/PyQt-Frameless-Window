# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from ..utils import startSystemMove
from .title_bar_buttons import CloseButton, MaximizeButton, MinimizeButton


class TitleBar(QWidget):
    """ Title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self.hBoxLayout = QHBoxLayout(self)
        self.__isDoubleClickEnabled = True

        self.resize(200, 32)
        self.setFixedHeight(32)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.Type.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.MouseButton.LeftButton or not self.__isDoubleClickEnabled:
            return

        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if sys.platform != "win32" or not self._isDragRegion(e.pos()):
            return

        startSystemMove(self.window(), e.globalPosition().toPoint())

    def mousePressEvent(self, e):
        if sys.platform == "win32" or e.button() != Qt.LeftButton or not self._isDragRegion(e.pos()):
            return

        startSystemMove(self.window(), e.globalPosition().toPoint())

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        return 0 < pos.x() < self.width() - 46 * 3

    def setDoubleClickEnabled(self, isEnabled):
        """ whether to switch window maximization status when double clicked

        Parameters
        ----------
        isEnabled: bool
            whether to enable double click
        """
        self.__isDoubleClickEnabled = isEnabled
