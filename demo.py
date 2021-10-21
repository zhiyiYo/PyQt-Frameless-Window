# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
from framelesswindow import FramelessWindow


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap("resource/images/硝子.png"))
        self.setWindowTitle("PyQt Frameless Window")
        self.setStyleSheet("background:white")
        self.titleBar.raise_()

    def resizeEvent(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        self.label.resize(length, length)
        self.label.move(
            self.width() // 2 - length // 2,
            self.height() // 2 - length // 2
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())
