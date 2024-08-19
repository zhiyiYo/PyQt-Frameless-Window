# coding:utf-8
import Cocoa
import objc
from PySide2.QtCore import QEvent, Qt, QRect, QSize, QPoint, QTimer
from PySide2.QtWidgets import QWidget

from ..titlebar import TitleBar
from .window_effect import MacWindowEffect


class MacFramelessWindow(QWidget):
    """ Frameless window for Linux system """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isSystemButtonVisible = False

    def _initFrameless(self):
        self.windowEffect = MacWindowEffect(self)
        # must enable acrylic effect before creating title bar
        if isinstance(self, AcrylicWindow):
            self.windowEffect.setAcrylicEffect(self.winId())

        self.titleBar = TitleBar(self)
        self._isResizeEnabled = True

        self.updateFrameless()

        self.resize(500, 500)
        self.titleBar.raise_()

    def updateFrameless(self):
        view = objc.objc_object(c_void_p=self.winId().__int__())
        self.__nsWindow = view.window()

        # hide system title bar
        self._hideSystemTitleBar()

    def setTitleBar(self, titleBar):
        """ set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.titleBar.deleteLater()
        self.titleBar.hide()
        self.titleBar = titleBar
        self.titleBar.setParent(self)
        self.titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def paintEvent(self, e):
        super().paintEvent(e)
        self._hideSystemTitleBar(self.isSystemButtonVisible())

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self._hideSystemTitleBar(self.isSystemButtonVisible())

            # Delay must be added, otherwise the buttons will be misplaced
            QTimer.singleShot(1, self._updateSystemButtonRect)
        elif event.type() == QEvent.Resize:
            self._updateSystemButtonRect()

    def _hideSystemTitleBar(self, showButton=False):
        # extend view to title bar region
        self.__nsWindow.setStyleMask_(
            self.__nsWindow.styleMask() | Cocoa.NSFullSizeContentViewWindowMask)
        self.__nsWindow.setTitlebarAppearsTransparent_(True)

        # disable the moving behavior of system
        self.__nsWindow.setMovableByWindowBackground_(False)
        self.__nsWindow.setMovable_(False)

        # hide title bar buttons and title
        self.__nsWindow.setTitleVisibility_(Cocoa.NSWindowTitleHidden)
        self.setSystemTitleBarButtonVisible(showButton)

    def isSystemButtonVisible(self):
        return self._isSystemButtonVisible

    def setSystemTitleBarButtonVisible(self, isVisible):
        self._isSystemButtonVisible = isVisible
        self.__nsWindow.setShowsToolbarButton_(isVisible)

        isHidden = not isVisible
        self.__nsWindow.standardWindowButton_(Cocoa.NSWindowCloseButton).setHidden_(isHidden)
        self.__nsWindow.standardWindowButton_(Cocoa.NSWindowZoomButton).setHidden_(isHidden)
        self.__nsWindow.standardWindowButton_(Cocoa.NSWindowMiniaturizeButton).setHidden_(isHidden)

        if isVisible:
            self._updateSystemButtonRect()

    def _updateSystemButtonRect(self):
        if not self.isSystemButtonVisible():
            return

        # get system title bar button
        leftButton = self.__nsWindow.standardWindowButton_(Cocoa.NSWindowCloseButton)
        midButton =  self.__nsWindow.standardWindowButton_(Cocoa.NSWindowMiniaturizeButton)
        rightButton = self.__nsWindow.standardWindowButton_(Cocoa.NSWindowZoomButton)

        # get system title bar
        titlebar = rightButton.superview()
        titlebarHeight = int(titlebar.frame().size.height)

        spacing = midButton.frame().origin.x - leftButton.frame().origin.x
        width = midButton.frame().size.width
        height = midButton.frame().size.height

        if self.__nsWindow.contentView():
            viewSize = self.__nsWindow.contentView().frame().size
        else:
            viewSize = self.__nsWindow.frame().size

        center = self.systemTitleBarRect(QSize(int(viewSize.width), titlebarHeight)).center()

        # The origin of the NSWindow coordinate system is in the lower left corner, we do the necessary transformations
        center.setY(titlebarHeight - center.y())

        # adjust the position of minimize button
        centerOrigin = Cocoa.NSPoint(center.x() - width // 2, center.y() - height // 2)
        midButton.setFrameOrigin_(centerOrigin)

        # adjust the position of close button
        leftOrigin = Cocoa.NSPoint(centerOrigin.x - spacing, centerOrigin.y)
        leftButton.setFrameOrigin_(leftOrigin)

        # adjust the position of zoom button
        rightOrigin = Cocoa.NSPoint(centerOrigin.x + spacing, centerOrigin.y)
        rightButton.setFrameOrigin_(rightOrigin)

    def systemTitleBarRect(self, size: QSize) -> QRect:
        """ Returns the system title bar rect

        Parameters
        ----------
        size: QSize
            original system title bar rect
        """
        return QRect(0, 0, 75, size.height())


class AcrylicWindow(MacFramelessWindow):
    """ A frameless window with acrylic effect """

    def _initFrameless(self):
        super()._initFrameless()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.windowEffect.setAcrylicEffect(self.winId())
        self.setStyleSheet("background: transparent")
