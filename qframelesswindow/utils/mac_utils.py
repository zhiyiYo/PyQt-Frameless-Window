# coding:utf-8
from ctypes import c_void_p

import Cocoa
import objc
from PySide6.QtCore import qVersion
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget
from Quartz.CoreGraphics import (CGEventCreateMouseEvent,
                                 kCGEventLeftMouseDown, kCGMouseButtonLeft)

QT_VERSION = tuple(int(v) for v in qVersion().split('.'))


class MacMoveResize:
    """ Tool class for moving and resizing Mac OS window """

    @staticmethod
    def startSystemMove(window: QWidget, globalPos):
        """ resize window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event
        """
        if QT_VERSION >= (5, 15, 0):
            window.windowHandle().startSystemMove()
            return

        nsWindow = getNSWindow(window.winId())

        # send click event
        cgEvent = CGEventCreateMouseEvent(
            None, kCGEventLeftMouseDown, (globalPos.x(), globalPos.y()), kCGMouseButtonLeft)
        clickEvent = Cocoa.NSEvent.eventWithCGEvent_(cgEvent)

        if clickEvent:
            nsWindow.performWindowDragWithEvent_(clickEvent)

        # CFRelease(cgEvent)

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
        pass


def getNSWindow(winId):
    """ convert window handle to NSWindow

    Parameters
    ----------
    winId: int or `sip.voidptr`
        window handle
    """
    view = objc.objc_object(c_void_p=c_void_p(int(winId)))
    return view.window()


def getSystemAccentColor():
    """ get the accent color of system

    Returns
    -------
    color: QColor
        accent color
    """
    color = Cocoa.NSColor.controlAccentColor()
    color = color.colorUsingColorSpace_(Cocoa.NSColorSpace.sRGBColorSpace())
    r = int(color.redComponent() * 255)
    g = int(color.greenComponent() * 255)
    b = int(color.blueComponent() * 255)
    return QColor(r, g, b)