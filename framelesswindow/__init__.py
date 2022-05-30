import sys

from .titlebar import TitleBar

if sys.platform == "win32":
    from .windows import AcrylicWindow, WindowsFramelessWindow, WindowsWindowEffect

    FramelessWindow = WindowsFramelessWindow
    WindowEffect = WindowsWindowEffect
else:
    from .unix import UnixFramelessWindow, UnixWindowEffect

    FramelessWindow = UnixFramelessWindow
    AcrylicWindow = UnixFramelessWindow
    WindowEffect = UnixWindowEffect
