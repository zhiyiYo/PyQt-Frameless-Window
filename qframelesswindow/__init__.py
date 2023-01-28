"""
PySide2-Frameless-Window
========================
A cross-platform frameless window based on pyside2, support Win32, Linux and macOS.

Documentation is available in the docstrings and
online at https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/Pyside2.

Examples are available at https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/Pyside2/examples.

:copyright: (c) 2021 by zhiyiYo.
:license: MIT, see LICENSE for more details.
"""

__version__ = "0.0.1"

import sys

from .titlebar import TitleBar, TitleBarButton, SvgTitleBarButton, StandardTitleBar

if sys.platform == "win32":
    from .windows import AcrylicWindow
    from .windows import WindowsFramelessWindow as FramelessWindow
    from .windows import WindowsWindowEffect as WindowEffect
elif sys.platform == "darwin":
    from .mac import AcrylicWindow
    from .mac import MacFramelessWindow as FramelessWindow
    from .mac import MacWindowEffect as WindowEffect
else:
    from .linux import LinuxFramelessWindow as FramelessWindow
    from .linux import LinuxWindowEffect as WindowEffect

    AcrylicWindow = FramelessWindow
