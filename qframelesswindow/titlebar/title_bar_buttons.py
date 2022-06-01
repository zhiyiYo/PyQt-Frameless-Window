# coding:utf-8
from PyQt5.QtCore import QPointF, QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QToolButton

from ..rc import resource


class TitleBarButton(QToolButton):
    """ Title bar button """

    def __init__(self, style=None, parent=None):
        """
        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color`, `background` and `icon`(close button only) attributes.

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
        self.updateStyle(style)
        self.setStyleSheet("""
            QToolButton{
                background-color: transparent;
                border: none;
                margin: 0px;
            }
        """)

    def updateStyle(self, style):
        """ update the style of button

        Parameters
        ----------
        style: dict
            button style of `normal`,`hover`, and `pressed`. Each state has
            `color`, `background` and `icon`(close button only) attributes.
        """
        style = style or {}
        for k, v in style.items():
            self._style[k].update(v)

        self.update()

    def setState(self, state):
        """ set the state of button

        Parameters
        ----------
        state: str
            the state of button, can be `normal`,`hover`, or `pressed`
        """
        if state not in ('normal', 'hover', 'pressed'):
            raise ValueError(
                'The state can only be `normal`,`hover`, or `pressed`')

        self._state = state
        self.update()

    def enterEvent(self, e):
        self.setState("hover")

    def leaveEvent(self, e):
        self.setState("normal")

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return

        self.setState("pressed")
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

    def __init__(self, style=None, parent=None):
        super().__init__(style, parent)
        self.__isMax = False

    def setMaxState(self, isMax):
        """ update the maximized state and icon """
        if self.__isMax == isMax:
            return

        self.__isMax = isMax
        self.setState("normal")

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

    def __init__(self, style=None, parent=None):
        defaultStyle = {
            "normal": {
                'background': (0, 0, 0, 0),
                "icon": ":/framelesswindow/close_black.svg"
            },
            "hover": {
                'background': (232, 17, 35),
                "icon": ":/framelesswindow/close_white.svg"
            },
            "pressed": {
                'background': (241, 112, 122),
                "icon": ":/framelesswindow/close_white.svg"
            },
        }
        super().__init__(defaultStyle, parent)
        self.updateStyle(style)
        self.setIconSize(QSize(46, 32))
        self.setIcon(QIcon(self._style['normal']['icon']))

    def updateStyle(self, style):
        super().updateStyle(style)
        self.setIcon(QIcon(self._style[self._state]['icon']))

    def enterEvent(self, e):
        self.setIcon(QIcon(self._style['hover']['icon']))
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setIcon(QIcon(self._style['normal']['icon']))
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        self.setIcon(QIcon(self._style['pressed']['icon']))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.setIcon(QIcon(self._style['normal']['icon']))
        super().mouseReleaseEvent(e)

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
