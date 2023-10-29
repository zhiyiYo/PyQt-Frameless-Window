# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from qframelesswindow import AcrylicWindow


class FramelessWebEngineView(QWebEngineView):
    """ Frameless web engine view """

    def __init__(self, parent):
        if sys.platform == "win32" and isinstance(parent, AcrylicWindow):
            parent.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        super().__init__(parent=parent)
        self.setHtml("")
        self.window().updateFrameless()