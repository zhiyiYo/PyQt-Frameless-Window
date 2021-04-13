# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
from framelesswindow import FramelessWindow


class Window(FramelessWindow):
    """ 测试无边框窗口 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('resource\\images\\硝子.png').scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # 设置层叠样式
        self.setStyleSheet('background:white')
        # 标题栏置顶
        self.titleBar.raise_()
        # 设置标题
        self.setWindowTitle('PyQt Frameless Window')

    def resizeEvent(self, e):
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        self.label.resize(length, length)
        self.label.setPixmap(QPixmap('resource\\images\\硝子.png').scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label.move(self.width()//2-length//2, self.height()//2-length//2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())
