# coding:utf-8
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG

import win32con
import win32gui
import win32api
from PySide6.QtCore import Qt, QSize, QRect, QPoint
from PySide6.QtGui import QCloseEvent, QCursor
from PySide6.QtWidgets import QApplication, QDialog, QWidget, QMainWindow

from ..titlebar import TitleBar
from ..utils import win32_utils as win_utils
from ..utils.win32_utils import Taskbar, isSystemBorderAccentEnabled, getSystemAccentColor
from .c_structures import LPNCCALCSIZE_PARAMS
from .window_effect import WindowsWindowEffect


class WindowsFramelessWindowBase:
    """ Frameless window base class for Windows system """

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isSystemButtonVisible = False
        self._isSystemMenuEnabled = True

    def _initFrameless(self):
        self.windowEffect = WindowsWindowEffect(self)
        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        self.updateFrameless()

        # solve issue #5
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)

        self.resize(500, 500)
        self.titleBar.raise_()
        if self._isSystemMenuEnabled:
            self._initSystemMenu()

    def updateFrameless(self):
        """ update frameless window """
        stayOnTop = Qt.WindowStaysOnTopHint if self.windowFlags() & Qt.WindowStaysOnTopHint else 0
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | stayOnTop)

        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self.winId())
        if not isinstance(self, AcrylicWindow):
            self.windowEffect.addShadowEffect(self.winId())

    def setTitleBar(self, titleBar):
        """ set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar.hide()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled
        if isEnabled:
            self.titleBar.maxBtn.setEnabled(True)
        else:
            self.titleBar.maxBtn.setEnabled(False)

    def setStayOnTop(self, isTop: bool):
        """ set the stay on top status """
        hWnd = int(self.winId())
        insert_after = win32con.HWND_TOPMOST if isTop else win32con.HWND_NOTOPMOST
        win32gui.SetWindowPos(hWnd, insert_after, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

    def toggleStayOnTop(self):
        """ toggle the stay on top status """
        hWnd = int(self.winId())
        info = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
        isTop = bool(info & win32con.WS_EX_TOPMOST)
        self.setStayOnTop(not isTop)

    def isSystemButtonVisible(self):
        """ Returns whether the system title bar button is visible """
        return self._isSystemButtonVisible

    def setSystemTitleBarButtonVisible(self, isVisible):
        """ set the visibility of system title bar button, only works for macOS """
        pass

    def systemTitleBarRect(self, size: QSize) -> QRect:
        """ Returns the system title bar rect, only works for macOS

        Parameters
        ----------
        size: QSize
            original system title bar rect
        """
        return QRect(0, 0, size.width(), size.height())

    def _isInTitleBar(self, pos: QPoint) -> bool:
        """Return if the Cursor is in the titleBar and its canDrag area"""
        pos = self.titleBar.mapFromGlobal(pos)
        return self.titleBar.rect().contains(pos) and self.titleBar.canDrag(pos)

    def _initSystemMenu(self):
        """Init system menu for Windows"""
        hWnd = int(self.winId())
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(hWnd, win32con.GWL_STYLE, style | win32con.WS_SYSMENU)

    def _showSystemMenu(self, point: QPoint, hWnd: int):
        """Show Windows system menu at the given point"""
        hMenu = win32gui.GetSystemMenu(hWnd, False)

        if self._isResizeEnabled:
            if win_utils.isMaximized(hWnd):
                win32gui.EnableMenuItem(hMenu, win32con.SC_MAXIMIZE, win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
                win32gui.EnableMenuItem(hMenu, win32con.SC_RESTORE,  win32con.MF_BYCOMMAND | win32con.MF_ENABLED)
                win32gui.EnableMenuItem(hMenu, win32con.SC_MOVE, win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
                win32gui.EnableMenuItem(hMenu, win32con.SC_SIZE, win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
            else:
                win32gui.EnableMenuItem(hMenu, win32con.SC_MAXIMIZE, win32con.MF_BYCOMMAND | win32con.MF_ENABLED)
                win32gui.EnableMenuItem(hMenu, win32con.SC_RESTORE,  win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
                win32gui.EnableMenuItem(hMenu, win32con.SC_MOVE, win32con.MF_BYCOMMAND | win32con.MF_ENABLED)
                win32gui.EnableMenuItem(hMenu, win32con.SC_SIZE, win32con.MF_BYCOMMAND | win32con.MF_ENABLED)
        else:
            win32gui.EnableMenuItem(hMenu, win32con.SC_MAXIMIZE, win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
            win32gui.EnableMenuItem(hMenu, win32con.SC_RESTORE,  win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
            win32gui.EnableMenuItem(hMenu, win32con.SC_MOVE, win32con.MF_BYCOMMAND | win32con.MF_GRAYED)
            win32gui.EnableMenuItem(hMenu, win32con.SC_SIZE, win32con.MF_BYCOMMAND | win32con.MF_GRAYED)

        ratio = self.devicePixelRatio()
        pos_x = int(point.x() * ratio)
        pos_y = int(point.y() * ratio)

        cmd = win32gui.TrackPopupMenu(hMenu, win32con.TPM_RETURNCMD | (win32con.TPM_RIGHTALIGN if QApplication.isRightToLeft() 
                                      else win32con.TPM_LEFTALIGN), pos_x, pos_y, 0, hWnd, None)

        if cmd:
            win32gui.PostMessage(hWnd, win32con.WM_SYSCOMMAND, cmd, 0)

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return False, 0

        if msg.message == win32con.WM_NCHITTEST:
            if self._isResizeEnabled:
                xPos, yPos = win32gui.ScreenToClient(msg.hWnd, win32api.GetCursorPos())
                clientRect = win32gui.GetClientRect(msg.hWnd)

                w = clientRect[2] - clientRect[0]
                h = clientRect[3] - clientRect[1]

                # fixes https://github.com/zhiyiYo/PyQt-Frameless-Window/issues/98
                bw = 0 if win_utils.isMaximized(msg.hWnd) or win_utils.isFullScreen(msg.hWnd) else self.BORDER_WIDTH
                lx = xPos < bw  # left
                rx = xPos > w - bw  # right
                ty = yPos < bw  # top
                by = yPos > h - bw  # bottom
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
                # Notify Windows that this region belongs to the title bar,
                # enabling system menu (right-click) and double-click to maximize/restore.
                elif self._isInTitleBar(QCursor.pos()):
                    return True, win32con.HTCAPTION
            else:
                if self._isSystemMenuEnabled and self._isInTitleBar(QCursor.pos()):
                    return True, win32con.HTCAPTION
        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            isMax = win_utils.isMaximized(msg.hWnd)
            isFull = win_utils.isFullScreen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                ty = win_utils.getResizeBorderThickness(msg.hWnd, False)
                rect.top += ty
                rect.bottom -= ty

                tx = win_utils.getResizeBorderThickness(msg.hWnd, True)
                rect.left += tx
                rect.right -= tx
                # Prevents flicker on right-clicking the title bar when the window is maximized.
                if self._isSystemMenuEnabled:
                    return True, 0

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and Taskbar.isAutoHide():
                position = Taskbar.getPosition(msg.hWnd)
                if position == Taskbar.LEFT:
                    rect.top += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.BOTTOM:
                    rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.LEFT:
                    rect.left += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.RIGHT:
                    rect.right -= Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result
        elif msg.message == win32con.WM_NCLBUTTONDBLCLK and msg.wParam == win32con.HTCAPTION:
            # enable/disable double click on titlebar
            if not self._isResizeEnabled or not self.titleBar._isDoubleClickEnabled:
                return True, 0
        elif self._isSystemMenuEnabled and msg.message == win32con.WM_SYSCHAR:
            if msg.wParam == win32con.VK_SPACE:
                self._showSystemMenu(self.pos(), msg.hWnd)
                return True, 0
        elif self._isSystemMenuEnabled and msg.message == win32con.WM_NCRBUTTONDOWN :
            if msg.wParam == win32con.HTCAPTION:
                self._showSystemMenu(QCursor.pos(), msg.hWnd)
                return True, 0
        elif msg.message == win32con.WM_SETFOCUS and isSystemBorderAccentEnabled():
            self.windowEffect.setBorderAccentColor(self.winId(), getSystemAccentColor())
            return True, 0
        elif msg.message == win32con.WM_KILLFOCUS:
            self.windowEffect.removeBorderAccentColor(self.winId())
            return True, 0

        return False, 0

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    def resizeEvent(self, e):
        self.titleBar.resize(self.width(), self.titleBar.height())


class WindowsFramelessWindow(WindowsFramelessWindowBase, QWidget):
    """  Frameless window for Windows system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()


class AcrylicWindow(WindowsFramelessWindow):
    """ A frameless window with acrylic effect """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__closedByKey = False

    def _initFrameless(self):
        super()._initFrameless()
        self.updateFrameless()

        self.setStyleSheet("AcrylicWindow{background:transparent}")

    def updateFrameless(self):
        stayOnTop = Qt.WindowStaysOnTopHint if self.windowFlags() & Qt.WindowStaysOnTopHint else 0
        self.setWindowFlags(Qt.FramelessWindowHint | stayOnTop)

        self.windowEffect.enableBlurBehindWindow(self.winId())
        self.windowEffect.addWindowAnimation(self.winId())

        self.windowEffect.setAcrylicEffect(self.winId())
        if win_utils.isGreaterEqualWin11():
            self.windowEffect.addShadowEffect(self.winId())

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())

        # handle Alt+F4
        if msg.message == win32con.WM_SYSKEYDOWN:
            if msg.wParam == win32con.VK_F4:
                self.__closedByKey = True
                QApplication.sendEvent(self, QCloseEvent())
                return False, 0

        return super().nativeEvent(eventType, message)

    def closeEvent(self, e):
        if not self.__closedByKey or QApplication.quitOnLastWindowClosed():
            self.__closedByKey = False
            return super().closeEvent(e)

        # system tray icon
        self.__closedByKey = False
        self.hide()


class WindowsFramelessMainWindow(WindowsFramelessWindowBase, QMainWindow):
    """ Frameless main window for Windows system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()


class WindowsFramelessDialog(WindowsFramelessWindowBase, QDialog):
    """ Frameless dialog for Windows system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initFrameless()
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
        self.windowEffect.disableMaximizeButton(self.winId())

