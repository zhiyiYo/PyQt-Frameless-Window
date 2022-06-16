# coding:utf-8
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

from qframelesswindow import FramelessWindow, TitleBar


class CustomTitleBar(TitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.label = QLabel('PyQt-Frameless-Window', self)
        self.label.setStyleSheet("QLabel{font: 13px 'Segoe UI'; margin: 10px}")
        self.label.adjustSize()

        # customize the style of title bar button
        self.minBtn.updateStyle({
            "hover": {
                "color": (0, 0, 0),
                'background': (0, 0, 0, 26)
            }
        })


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        # self.setTitleBar(CustomTitleBar(self))

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap("screenshot/shoko.png"))
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
    sys.exit(app.exec())
