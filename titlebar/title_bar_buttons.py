# coding:utf-8

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton


class MaximizeButton(QToolButton):
    """ 最大化按钮 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconPathDict_list = [
            {'normal': r'resource\images\title_bar\最大化按钮_normal_57_40.png',
             'hover': r'resource\images\title_bar\最大化按钮_hover_57_40.png',
             'pressed': r'resource\images\title_bar\最大化按钮_pressed_57_40.png'},
            {'normal': r'resource\images\title_bar\向下还原按钮_normal_57_40.png',
             'hover': r'resource\images\title_bar\向下还原按钮_hover_57_40.png',
             'pressed': r'resource\images\title_bar\向下还原按钮_pressed_57_40.png'}
        ]
        self.resize(57, 40)
        # 设置标志位
        self.isMax = False
        self.setIcon(QIcon(r'resource\images\title_bar\最大化按钮_normal_57_40.png'))
        self.setIconSize(QSize(57, 40))

    def __updateIcon(self, iconState: str):
        """ 更新图标 """
        self.setIcon(
            QIcon(self.iconPathDict_list[self.isMax][iconState]))

    def enterEvent(self, e):
        """ hover时更换图标 """
        self.__updateIcon('hover')

    def leaveEvent(self, e):
        """ leave时更换图标 """
        self.__updateIcon('normal')

    def mousePressEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.__updateIcon('pressed')
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """ 鼠标松开时更换按钮图标 """
        if e.button() == Qt.RightButton:
            return
        self.isMax = not self.isMax
        self.__updateIcon('normal')
        super().mouseReleaseEvent(e)

    def setMaxState(self, isMax: bool):
        """ 更新最大化标志位和图标 """
        self.isMax = isMax
        self.__updateIcon('normal')


class ThreeStateToolButton(QToolButton):
    """ 三种状态对应三种图标的按钮，iconPath_dict提供按钮normal、hover、pressed三种状态下的图标地址 """

    def __init__(self, iconPath_dict: dict, icon_size: tuple = (50, 50), parent=None):
        super().__init__(parent)
        # 引用图标地址字典
        self.iconPath_dict = iconPath_dict
        self.resize(*icon_size)
        # 初始化小部件
        self.initWidget()

    def initWidget(self):
        """ 初始化小部件 """
        self.setCursor(Qt.ArrowCursor)
        self.setIcon(QIcon(self.iconPath_dict['normal']))
        self.setIconSize(QSize(self.width(), self.height()))
        self.setStyleSheet('border: none; margin: 0px')

    def enterEvent(self, e):
        """ hover时更换图标 """
        self.setIcon(QIcon(self.iconPath_dict['hover']))

    def leaveEvent(self, e):
        """ leave时更换图标 """
        self.setIcon(QIcon(self.iconPath_dict['normal']))

    def mousePressEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.setIcon(QIcon(self.iconPath_dict['pressed']))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.setIcon(QIcon(self.iconPath_dict['normal']))
        super().mouseReleaseEvent(e)
