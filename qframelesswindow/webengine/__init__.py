from PySide6.QtWebEngineWidgets import QWebEngineView


class FramelessWebEngineView(QWebEngineView):
    """ Frameless web engine view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setHtml("")
        self.window().updateFrameless()