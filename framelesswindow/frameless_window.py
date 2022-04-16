# coding:utf-8
from ctypes import POINTER, cast
from ctypes.wintypes import MSG

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWinExtras import QtWin
from win32 import win32api, win32gui
from win32.lib import win32con

from titlebar import TitleBar
from windoweffect import WindowEffect, MINMAXINFO, NCCALCSIZE_PARAMS


class FramelessWindow(QWidget):

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__monitorInfo = None
        self.titleBar = TitleBar(self)
        self.windowEffect = WindowEffect()

        # remove window border
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self.winId())
        self.windowEffect.addShadowEffect(self.winId())

        # solve issue #5
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)

        self.resize(500, 500)
        self.titleBar.raise_()

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w, h = self.width(), self.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos > w - self.BORDER_WIDTH
            ty = yPos < self.BORDER_WIDTH
            by = yPos > h - self.BORDER_WIDTH
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if self.__isWindowMaximized(msg.hWnd):
                self.__monitorNCCALCSIZE(msg)
            return True, 0
        elif msg.message == win32con.WM_GETMINMAXINFO:
            if self.__isWindowMaximized(msg.hWnd):
                window_rect = win32gui.GetWindowRect(msg.hWnd)
                if not window_rect:
                    return False, 0

                # get the monitor handle
                monitor = win32api.MonitorFromRect(window_rect)
                if not monitor:
                    return False, 0

                # get the monitor info
                __monitorInfo = win32api.GetMonitorInfo(monitor)
                monitor_rect = __monitorInfo['Monitor']
                work_area = __monitorInfo['Work']

                # convert lParam to MINMAXINFO pointer
                info = cast(msg.lParam, POINTER(MINMAXINFO)).contents

                # adjust the size of window
                info.ptMaxSize.x = work_area[2] - work_area[0]
                info.ptMaxSize.y = work_area[3] - work_area[1]
                info.ptMaxTrackSize.x = info.ptMaxSize.x
                info.ptMaxTrackSize.y = info.ptMaxSize.y

                # modify the upper left coordinate
                info.ptMaxPosition.x = abs(window_rect[0] - monitor_rect[0])
                info.ptMaxPosition.y = abs(window_rect[1] - monitor_rect[1])
                return True, 1

        return QWidget.nativeEvent(self, eventType, message)

    def resizeEvent(self, e):
        """ Adjust the width and icon of title bar """
        super().resizeEvent(e)
        self.titleBar.resize(self.width(), 40)
        # update the maximized icon
        self.titleBar.maxBtn.setMaxState(
            self.__isWindowMaximized(int(self.winId())))

    def __isWindowMaximized(self, hWnd) -> bool:
        """ Determine whether the window is maximized """
        # GetWindowPlacement() returns the display state of the window and the restored,
        # maximized and minimized window position. The return value is tuple
        windowPlacement = win32gui.GetWindowPlacement(hWnd)
        if not windowPlacement:
            return False

        return windowPlacement[1] == win32con.SW_MAXIMIZE

    def __monitorNCCALCSIZE(self, msg: MSG):
        """ Adjust the size of window """
        monitor = win32api.MonitorFromWindow(msg.hWnd)

        # If the display information is not saved, return directly
        if monitor is None and not self.__monitorInfo:
            return
        elif monitor is not None:
            self.__monitorInfo = win32api.GetMonitorInfo(monitor)

        # adjust the size of window
        params = cast(msg.lParam, POINTER(NCCALCSIZE_PARAMS)).contents
        params.rgrc[0].left = self.__monitorInfo['Work'][0]
        params.rgrc[0].top = self.__monitorInfo['Work'][1]
        params.rgrc[0].right = self.__monitorInfo['Work'][2]
        params.rgrc[0].bottom = self.__monitorInfo['Work'][3]

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)


class AcrylicWindow(FramelessWindow):
    """ A frameless window with acrylic effect """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        QtWin.enableBlurBehindWindow(self)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowMinMaxButtonsHint)
        self.windowEffect.addWindowAnimation(self.winId())
        self.windowEffect.setAcrylicEffect(self.winId())
        self.setStyleSheet("background:transparent")
