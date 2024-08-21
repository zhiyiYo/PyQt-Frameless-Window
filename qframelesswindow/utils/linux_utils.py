# coding: utf-8
from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent, QColor
from PySide6.QtWidgets import QApplication


class LinuxMoveResize:
    """ Tool class for moving and resizing window """

    @classmethod
    def startSystemMove(cls, window, globalPos):
        """ move window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event
        """
        window.windowHandle().startSystemMove()
        event = QMouseEvent(QEvent.MouseButtonRelease, QPoint(-1, -1),
                            Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
        QApplication.instance().postEvent(window.windowHandle(), event)

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        """ resize window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event

        edges: `Qt.Edges`
            window edges
        """
        if not edges:
            return

        window.windowHandle().startSystemResize(edges)


def getSystemAccentColor():
    """ get the accent color of system

    Returns
    -------
    color: QColor
        accent color
    """
    return QColor()