# PyQt Frameless Window

## Features
* Move
* Stretching
* Window animation
* Window DWM shadow
* Win10 acrylic blur
* Win7 Aero blur

## Examples
* Normal frameless window
![Normal Frameless Window](screenshot/normal_frameless_window.gif)
* Acrylic frameless window
![Acrylic Frameless Window](screenshot/Acrylic_window.gif)

## Blog
[《如何在pyqt中自定义无边框窗口》](https://www.cnblogs.com/zhiyiYo/p/14659981.html)

## Notes
1. `FramelessWindow` provides a custom title bar. If you don't like it, you can rewrite it;
2. The default style of `FramelessWindow` is borderless window with DWM shadow. If you want other special effects, such as acrylic effect, you can rewrite the `__init__()` function of `FramelessWindow`. Here is an example:

    ```python
    def __init__(self, parent=None):
        super().__init__(parent)
        self.monitor_info = None
        self.titleBar = TitleBar(self)
        self.windowEffect = WindowEffect()
        # remove border
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setStyleSheet('background:transparent')
        # Add window animation and acrylic blur
        self.windowEffect.addWindowAnimation(self.winId())
        self.windowEffect.setAcrylicEffect(self.winId())
        self.resize(500, 500)
        self.titleBar.raise_()
    ```
3. The window using the acrylic effect may be stuck when dragging. See the blog for solution.

## License
```
MIT License

Copyright (c) 2021 Zhengzhi Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
