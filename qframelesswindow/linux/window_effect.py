# coding:utf-8
import subprocess

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class LinuxWindowEffect:
    """ Linux window effect """

    def __init__(self, window):
        self.window = window

    def setAcrylicEffect(self, hWnd, gradientColor="F2F2F230", isEnableShadow=True, animationId=0):
        """ set acrylic effect for window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            window handle

        gradientColor: str
            hexadecimal acrylic mixed color, corresponding to RGBA components

        isEnableShadow: bool
            whether to enable window shadow

        animationId: int
            turn on blur animation or not
        """
        self.setTransparentEffect(hWnd)
        self.enableBlurBehindWindow(hWnd)

    def setBorderAccentColor(self, hWnd, color: QColor):
        """ Set the border color of the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        color: QColor
            Border Accent color
        """
        pass

    def removeBorderAccentColor(self, hWnd):
        """ Remove the border color of the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    def setMicaEffect(self, hWnd, isDarkMode=False, isAlt=False):
        """ Add mica effect to the window (Win11 only)

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        isDarkMode: bool
            whether to use dark mode mica effect

        isAlt: bool
            whether to use mica alt effect
        """
        self.setAcrylicEffect(hWnd)

    def setAeroEffect(self, hWnd):
        """ add Aero effect to the window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        self.enableBlurBehindWindow(hWnd)

    def setTransparentEffect(self, hWnd):
        """ set transparent effect for window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        self.window.setAttribute(Qt.WA_TranslucentBackground)

    def removeBackgroundEffect(self, hWnd):
        """ Remove background effect

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        self.window.setAttribute(Qt.WA_TranslucentBackground, False)
        self.disableBlurBehindWindow(hWnd)

    def addShadowEffect(self, hWnd):
        """ add shadow to window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    def addMenuShadowEffect(self, hWnd):
        """ add shadow to menu

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    @staticmethod
    def removeMenuShadowEffect(hWnd):
        """ Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    def removeShadowEffect(self, hWnd):
        """ Remove shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    @staticmethod
    def addWindowAnimation(hWnd):
        """ Enables the maximize and minimize animation of the window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        pass

    @staticmethod
    def disableMaximizeButton(hWnd):
        """ Disable the maximize button of window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        pass

    def enableBlurBehindWindow(self, hWnd):
        """ enable the blur effect behind the whole client

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        try:
            wid = int(self.window.winId())
            subprocess.Popen(
                ['xprop', '-id', str(wid),
                 '-f', '_KDE_NET_WM_BLUR_BEHIND_REGION', '32c',
                 '-set', '_KDE_NET_WM_BLUR_BEHIND_REGION', '0'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    def removeWindowAnimation(self, hWnd):
        """ Disables maximize and minimize animation of the window by removing the relevant window styles.

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    def disableBlurBehindWindow(self, hWnd):
        """ disable the blur effect behind the whole client

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        try:
            wid = int(self.window.winId())
            subprocess.Popen(
                ['xprop', '-id', str(wid),
                 '-remove', '_KDE_NET_WM_BLUR_BEHIND_REGION'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass