# coding: utf-8
import sys

from PySide2.QtCore import Qt
from PySide2.QtWebEngineWidgets import QWebEngineView
from qframelesswindow import AcrylicWindow, FramelessWindowBase


class FramelessWebEngineView(QWebEngineView):
    """ Frameless web engine view """

    def __init__(self, parent):
        if sys.platform == "win32" and isinstance(parent.window(), AcrylicWindow):
            parent.window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        super().__init__(parent=parent)
        self.setHtml("")

        if isinstance(self.window(), FramelessWindowBase):
            self.window().updateFrameless()