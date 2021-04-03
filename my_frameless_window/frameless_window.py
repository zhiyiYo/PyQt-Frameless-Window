# coding:utf-8

from ctypes import POINTER, cast
from ctypes.wintypes import MSG

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from win32 import win32api, win32gui
from win32.lib import win32con

from my_title_bar import TitleBar
from my_window_effect.window_effect import WindowEffect
from my_window_effect.c_structures import MINMAXINFO, NCCALCSIZE_PARAMS


class FramelessWindow(QWidget):

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.monitor_info = None
        self.titleBar = TitleBar(self)
        self.windowEffect = WindowEffect()
        # 取消边框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        # 添加阴影和窗口动画
        self.windowEffect.addShadowEffect(self.winId())
        self.windowEffect.addWindowAnimation(self.winId())
        self.resize(500, 500)
        self.titleBar.raise_()

    def isWindowMaximized(self, hWnd) -> bool:
        """ 判断窗口是否最大化 """
        # 返回指定窗口的显示状态以及被恢复的、最大化的和最小化的窗口位置，返回值为元组
        windowPlacement = win32gui.GetWindowPlacement(hWnd)
        if not windowPlacement:
            return False
        return windowPlacement[1] == win32con.SW_MAXIMIZE

    def resizeEvent(self, e):
        self.titleBar.resize(self.width(), 40)

    def nativeEvent(self, eventType, message):
        """ 处理windows消息 """
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST:
            xPos = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
            yPos = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            w, h = self.width(), self.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos + 9 > w - self.BORDER_WIDTH
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
            if self.isWindowMaximized(msg.hWnd):
                self.monitorNCCALCSIZE(msg)
            return True, 0
        elif msg.message == win32con.WM_GETMINMAXINFO:
            if self.isWindowMaximized(msg.hWnd):
                window_rect = win32gui.GetWindowRect(msg.hWnd)
                if not window_rect:
                    return False, 0
                # 获取显示器句柄
                monitor = win32api.MonitorFromRect(window_rect)
                if not monitor:
                    return False, 0
                # 获取显示器信息
                monitor_info = win32api.GetMonitorInfo(monitor)
                monitor_rect = monitor_info['Monitor']
                work_area = monitor_info['Work']
                # 将lParam转换为MINMAXINFO指针
                info = cast(msg.lParam, POINTER(MINMAXINFO)).contents
                # 调整窗口大小
                info.ptMaxSize.x = work_area[2] - work_area[0]
                info.ptMaxSize.y = work_area[3] - work_area[1]
                info.ptMaxTrackSize.x = info.ptMaxSize.x
                info.ptMaxTrackSize.y = info.ptMaxSize.y
                # 修改左上角坐标
                info.ptMaxPosition.x = abs(window_rect[0] - monitor_rect[0])
                info.ptMaxPosition.y = abs(window_rect[1] - monitor_rect[1])
                return True, 1
        return QWidget.nativeEvent(self, eventType, message)

    def resizeEvent(self, e):
        """ 改变标题栏大小 """
        super().resizeEvent(e)
        self.titleBar.resize(self.width(), 40)
        # 更新最大化按钮图标
        if self.isWindowMaximized(int(self.winId())):
            self.titleBar.maxBt.setMaxState(True)

    def monitorNCCALCSIZE(self, msg: MSG):
        """ 调整窗口大小 """
        monitor = win32api.MonitorFromWindow(msg.hWnd)
        # 如果没有保存显示器信息就直接返回，否则接着调整窗口大小
        if monitor is None and not self.monitor_info:
            return
        elif monitor is not None:
            self.monitor_info = win32api.GetMonitorInfo(monitor)
        # 调整窗口大小
        params = cast(msg.lParam, POINTER(NCCALCSIZE_PARAMS)).contents
        params.rgrc[0].left = self.monitor_info['Work'][0]
        params.rgrc[0].top = self.monitor_info['Work'][1]
        params.rgrc[0].right = self.monitor_info['Work'][2]
        params.rgrc[0].bottom = self.monitor_info['Work'][3]
