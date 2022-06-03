import sys

if sys.platform == "win32":
    from .titlebar import WindowsTitleBar as TitleBar
    from .windows import AcrylicWindow
    from .windows import WindowsFramelessWindow as FramelessWindow
    from .windows import WindowsWindowEffect as WindowEffect
else:
    from .titlebar import UnixTitleBar as TitleBar
    from .unix import UnixFramelessWindow as FramelessWindow
    from .unix import UnixWindowEffect as WindowEffect

    AcrylicWindow = FramelessWindow
