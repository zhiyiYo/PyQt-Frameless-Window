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

## Blogs
* [如何在pyqt中通过调用SetWindowCompositionAttribute实现Win10亚克力效果](https://blog.csdn.net/zhiyiYo/article/details/107891876?spm=1001.2014.3001.5501)
* [如何在pyqt中给无边框窗口添加DWM环绕阴影](https://blog.csdn.net/zhiyiYo/article/details/114736952?spm=1001.2014.3001.5501)
* [如何在pyqt中在实现无边框窗口的同时保留Windows窗口动画效果（一）](https://blog.csdn.net/zhiyiYo/article/details/107883478?spm=1001.2014.3001.5501)
* [如何在pyqt中在实现无边框窗口的同时保留Windows窗口动画效果（二）](https://blog.csdn.net/zhiyiYo/article/details/114752515?spm=1001.2014.3001.5501)

## Notes
1. `FramelessWindow` provides a custom title bar. If you don't like it, you can rewrite it;
2. The default style of `FramelessWindow` is borderless window with DWM shadow. If you want other special effects, such as acrylic effect, you can rewrite the `__init__()` function of `FramelessWindow`. Here is an example:
```python
def __init__(self, parent=None):
    super().__init__(parent)
    self.monitor_info = None
    self.titleBar = TitleBar(self)
    self.windowEffect = WindowEffect()
    # 取消边框
    self.setWindowFlags(Qt.FramelessWindowHint)
    self.setStyleSheet('background:transparent')
    # 添加阴影和窗口动画
    self.windowEffect.setAcrylicEffect(self.winId())
    self.resize(500, 500)
    self.titleBar.raise_()
```
