# coding:utf-8
import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QHBoxLayout

from qframelesswindow import FramelessWindow, TitleBar, StandardTitleBar
from qframelesswindow.webengine import FramelessWebEngineView


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.setTitleBar(StandardTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)

        # must replace QWebEngineView with FramelessWebEngineView
        self.webEngine = FramelessWebEngineView(self)

        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.webEngine)

        # load web page
        self.webEngine.load(QUrl("https://qfluentwidgets.com/"))
        self.resize(1200, 800)

        self.titleBar.raise_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    app.exec()
