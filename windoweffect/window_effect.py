# coding:utf-8
import sys

from ctypes import POINTER, c_bool, c_int, pointer, sizeof, WinDLL, byref
from ctypes.wintypes import DWORD, LONG, LPCVOID

from win32 import win32api, win32gui
from win32.lib import win32con

from .c_structures import (
    ACCENT_POLICY,
    ACCENT_STATE,
    MARGINS,
    DWMNCRENDERINGPOLICY,
    DWMWINDOWATTRIBUTE,
    WINDOWCOMPOSITIONATTRIB,
    WINDOWCOMPOSITIONATTRIBDATA,
)


class WindowEffect:
    """ A class that calls Windows API to realize window effect """

    def __init__(self):
        # Declare the function signature of the API
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute
        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG
        self.SetWindowCompositionAttribute.argtypes = [
            c_int,
            POINTER(WINDOWCOMPOSITIONATTRIBDATA),
        ]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]

        # Initialize structure
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        self.winCompAttrData.Data = pointer(self.accentPolicy)

    def setAcrylicEffect(self, hWnd, gradientColor: str = "F2F2F299", isEnableShadow: bool = True, animationId: int = 0):
        """ Add the acrylic effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        gradientColor: str
            Hexadecimal acrylic mixed color, corresponding to four RGBA channels

        isEnableShadow: bool
            Enable window shadows

        animationId: int
            Turn on matte animation
        """
        hWnd = int(hWnd)
        # Acrylic mixed color
        gradientColor = (
            gradientColor[6:]
            + gradientColor[4:6]
            + gradientColor[2:4]
            + gradientColor[:2]
        )
        gradientColor = DWORD(int(gradientColor, base=16))
        # matte animation
        animationId = DWORD(animationId)
        # window shadow
        accentFlags = DWORD(0x20 | 0x40 | 0x80 |
                            0x100) if isEnableShadow else DWORD(0)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        # enable acrylic effect
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def setMicaEffect(self, hWnd):
        """ Add the mica effect to the window (Win11 only)

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        if sys.getwindowsversion().build < 22000:
            raise Exception("The mica effect is only available on Win11")

        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))
        self.DwmSetWindowAttribute(hWnd, 1029, byref(c_int(1)), 4)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_HOSTBACKDROP.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def setAeroEffect(self, hWnd):
        """ Add the aero effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def removeBackgroundEffect(self, hWnd):
        """ Remove background effect

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    @staticmethod
    def moveWindow(hWnd):
        """ Move the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            hWnd, win32con.WM_SYSCOMMAND, win32con.SC_MOVE + win32con.HTCAPTION, 0
        )

    def addShadowEffect(self, hWnd):
        """ Add DWM shadow to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_ENABLED.value)),
            4,
        )
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    def removeShadowEffect(self, hWnd):
        """ Remove DWM shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_DISABLED.value)),
            4,
        )

    @staticmethod
    def removeMenuShadowEffect(hWnd):
        """ Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        style = win32gui.GetClassLong(hWnd, win32con.GCL_STYLE)
        style &= ~0x00020000  # CS_DROPSHADOW
        win32api.SetClassLong(hWnd, win32con.GCL_STYLE, style)

    @staticmethod
    def addWindowAnimation(hWnd):
        """ Enables the maximize and minimize animation of the window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )
