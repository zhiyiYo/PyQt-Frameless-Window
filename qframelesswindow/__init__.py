import sys

if sys.platform == "win32":
    from .titlebar import WindowsTitleBar as TitleBar
    from .windows import AcrylicWindow
    from .windows import WindowsFramelessWindow as FramelessWindow
    from .windows import WindowsWindowEffect as WindowEffect
elif sys.platform == "darwin":
    from .titlebar import MacTitleBar as TitleBar
    from .mac import AcrylicWindow
    from .mac import MacFramelessWindow as FramelessWindow
    from .mac import MacWindowEffect as WindowEffect
else:
    from .titlebar import LinuxTitleBar as TitleBar
    from .linux import LinuxFramelessWindow as FramelessWindow
    from .linux import LinuxWindowEffect as WindowEffect

    AcrylicWindow = FramelessWindow
