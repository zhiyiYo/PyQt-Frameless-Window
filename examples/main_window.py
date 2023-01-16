# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMenuBar, QMenu, QStatusBar, QTextEdit, QHBoxLayout

from qframelesswindow import FramelessMainWindow, FramelessDialog


class MainWindow(FramelessMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frameless Main Window")

        # add menu bar
        menuBar = QMenuBar(self.titleBar)
        menu = QMenu('File(&F)', self)
        menu.addAction('open')
        menu.addAction('save')
        menuBar.addMenu(menu)
        menuBar.addAction('Edit(&E)')
        menuBar.addAction('Select(&S)')
        menuBar.addAction('Help(&H)', self.showHelpDialog)
        self.titleBar.layout().insertWidget(0, menuBar, 0, Qt.AlignLeft)
        self.titleBar.layout().insertStretch(1, 1)
        self.setMenuWidget(self.titleBar)

        # add status bar
        statusBar = QStatusBar(self)
        statusBar.addWidget(QLabel('row 1'))
        statusBar.addWidget(QLabel('column 1'))
        self.setStatusBar(statusBar)

        # set central widget
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.setStyleSheet("""
            QMenuBar{background: #F0F0F0; padding: 5px 0}
            QTextEdit{border: none; font-size: 15px}
            QDialog > QLabel{font-size: 15px}
        """)

    def showHelpDialog(self):
        w = FramelessDialog(self)

        # add a label to dialog
        w.setLayout(QHBoxLayout())
        w.layout().addWidget(QLabel('Frameless Dialog'), 0, Qt.AlignCenter)

        # raise title bar
        w.titleBar.raise_()
        w.resize(300, 300)

        # disable resizing dialog
        w.setResizeEnabled(False)
        w.exec()


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
