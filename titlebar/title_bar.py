# coding:utf-8

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QToolButton, QWidget
from win32.lib import win32con
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture

from .title_bar_buttons import MaximizeButton, ThreeStateToolButton


class TitleBar(QWidget):
    """ 定义标题栏 """

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(1360, 40)
        # 创建记录下标的列表，里面的每一个元素为元组，第一个元素为stackWidget名字，第二个为Index
        self.stackWidgetIndex_list = []
        # 实例化小部件
        self.__createButtons()
        # 初始化界面
        self.__initWidget()
        self.__adjustButtonPos()

    def __createButtons(self):
        """ 创建各按钮 """
        self.minBt = ThreeStateToolButton(
            {'normal': r'resource\images\title_bar\最小化按钮_normal_57_40.png',
             'hover': r'resource\images\title_bar\最小化按钮_hover_57_40.png',
             'pressed': r'resource\images\title_bar\最小化按钮_pressed_57_40.png'}, (57, 40), self)
        self.closeBt = ThreeStateToolButton(
            {'normal': r'resource\images\title_bar\关闭按钮_normal_57_40.png',
             'hover': r'resource\images\title_bar\关闭按钮_hover_57_40.png',
             'pressed': r'resource\images\title_bar\关闭按钮_pressed_57_40.png'}, (57, 40), self)
        self.maxBt = MaximizeButton(self)
        self.button_list = [self.minBt, self.maxBt, self.closeBt]

    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedHeight(40)
        self.setAttribute(Qt.WA_StyledBackground)
        self.__setQss()
        # 将按钮的点击信号连接到槽函数
        self.minBt.clicked.connect(self.window().showMinimized)
        self.maxBt.clicked.connect(self.__showRestoreWindow)
        self.closeBt.clicked.connect(self.window().close)

    def __adjustButtonPos(self):
        """ 初始化小部件位置 """
        self.closeBt.move(self.width() - 57, 0)
        self.maxBt.move(self.width() - 2 * 57, 0)
        self.minBt.move(self.width() - 3 * 57, 0)

    def resizeEvent(self, e: QResizeEvent):
        """ 尺寸改变时移动按钮 """
        self.__adjustButtonPos()

    def mouseDoubleClickEvent(self, event):
        """ 双击最大化窗口 """
        self.__showRestoreWindow()

    def mousePressEvent(self, event):
        """ 移动窗口 """
        # 判断鼠标点击位置是否允许拖动
        if self.__isPointInDragRegion(event.pos()):
            ReleaseCapture()
            SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                        win32con.SC_MOVE + win32con.HTCAPTION, 0)
            event.ignore()

    def __showRestoreWindow(self):
        """ 复原窗口并更换最大化按钮的图标 """
        if self.window().isMaximized():
            self.window().showNormal()
            # 更新标志位用于更换图标
            self.maxBt.setMaxState(False)
        else:
            self.window().showMaximized()
            self.maxBt.setMaxState(True)

    def __isPointInDragRegion(self, pos) -> bool:
        """ 检查鼠标按下的点是否属于允许拖动的区域 """
        x = pos.x()
        # 如果最小化按钮看不见也意味着最大化按钮看不见
        right = self.width() - 57 * 3 if self.minBt.isVisible() else self.width() - 57
        return (0 < x < right)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\title_bar.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
