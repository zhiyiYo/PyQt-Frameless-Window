# coding: utf-8
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QWidget


class LinuxMoveResize:
    """ Tool class for moving and resizing window """

    moveResizeAtom = None

    @classmethod
    def startSystemMove(cls, window, globalPos):
        """ move window """
        window.windowHandle().startSystemMove()

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
        window.windowHandle().startSystemResize(edges)
