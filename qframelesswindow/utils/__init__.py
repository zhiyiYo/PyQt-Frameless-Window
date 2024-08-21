# coding:utf-8
import sys

if sys.platform == "win32":
    from .win32_utils import WindowsMoveResize as MoveResize
    from .win32_utils import getSystemAccentColor
elif sys.platform == "darwin":
    from .mac_utils import MacMoveResize as MoveResize
    from .mac_utils import getSystemAccentColor
else:
    from .linux_utils import LinuxMoveResize as MoveResize
    from .linux_utils import getSystemAccentColor


def startSystemMove(window, globalPos):
    """ resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event
    """
    MoveResize.startSystemMove(window, globalPos)


def starSystemResize(window, globalPos, edges):
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
    MoveResize.starSystemResize(window, globalPos, edges)
