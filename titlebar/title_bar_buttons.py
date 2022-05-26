# coding:utf-8
from PyQt5.QtCore import QPointF, QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QToolButton


class TitleBarButton(QToolButton):
    """ Title bar button """

    def __init__(self, style: dict = None, parent=None):
        """
        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color` and `background` attributes.

        parent:
            parent widget
        """
        super().__init__(parent=parent)
        self.setCursor(Qt.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = 'normal'
        self._style = {
            "normal": {
                "color": (0, 0, 0, 255),
                'background': (0, 0, 0, 0)
            },
            "hover": {
                "color": (255, 255, 255),
                'background': (0, 100, 182)
            },
            "pressed": {
                "color": (255, 255, 255),
                'background': (54, 57, 65)
            },
        }
        self._style.update(style or {})
        self.setStyleSheet("""
            QToolButton{
                background-color: transparent;
                border: none;
                margin: 0px;
            }
        """)

    def enterEvent(self, e):
        self._state = 'hover'
        self.update()

    def leaveEvent(self, e):
        self._state = 'normal'
        self.update()

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return

        self._state = 'pressed'
        self.update()
        super().mousePressEvent(e)


class MinimizeButton(TitleBarButton):
    """ Minimize button """

    def paintEvent(self, e):
        painter = QPainter(self)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QColor(*style['background']))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(QColor(*style['color']), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    """ Maximize button """

    def __init__(self, style: dict = None, parent=None):
        super().__init__(style, parent)
        self.__isMax = False

    def setMaxState(self, isMax: bool):
        """ update the maximized state and icon """
        if self.__isMax == isMax:
            return

        self.__isMax = isMax
        self._state = "normal"
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QColor(*style['background']))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(QColor(*style['color']), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self.__isMax:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)


class CloseButton(TitleBarButton):
    """ Close button """

    def __init__(self, style: dict = None, parent=None):
        defaultStyle = {
            "normal": {
                'background': (0, 0, 0, 0)
            },
            "hover": {
                'background': (232, 17, 35)
            },
            "pressed": {
                'background': (241, 112, 122)
            },
        }
        defaultStyle.update(style or {})
        super().__init__(defaultStyle, parent)
        self.setIconSize(QSize(46, 32))
        self.setIcon(QIcon('resource/images/title_bar/button_close_black.svg'))

    def enterEvent(self, e):
        self.setIcon(QIcon('resource/images/title_bar/button_close_white.svg'))
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setIcon(QIcon('resource/images/title_bar/button_close_black.svg'))
        super().leaveEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # draw background
        style = self._style[self._state]
        painter.setBrush(QColor(*style['background']))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        super().paintEvent(e)
