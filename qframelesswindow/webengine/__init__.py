# coding: utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qframelesswindow import AcrylicWindow, FramelessWindow


class FramelessWebEngineView(QWebEngineView):
    """ Frameless web engine view """

    def __init__(self, parent):
        if sys.platform == "win32" and isinstance(parent.window(), AcrylicWindow):
            parent.window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        super().__init__(parent=parent)
        self.setHtml("")

        if isinstance(self.window(), FramelessWindow):
            self.window().updateFrameless()