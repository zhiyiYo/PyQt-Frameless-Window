# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from qframelesswindow import FramelessWindow
from qframelesswindow.utils import ScreenCaptureFilter



class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("PyQt-Frameless-Window")

        # disable screen capture
        self.installEventFilter(ScreenCaptureFilter(self))



if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())
