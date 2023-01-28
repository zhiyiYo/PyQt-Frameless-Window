# coding: utf-8

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
