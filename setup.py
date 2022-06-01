import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PyQt5-Frameless-Window",
    version="0.0.5",
    keywords="pyqt frameless",
    author="Huang Zhengzhi",
    author_email="1319158137@qq.com",
    description="A cross-platform frameless window based on pyqt5, support Win32, X11, Wayland and macOS.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/zhiyiYo/PyQt-Frameless-Window",
    packages=setuptools.find_packages(),
    install_requires=[
        "pywin32 >= 227,<=300;platform_system=='Windows'",
        "xcffib >= 0.11.1;platform_system!='Windows'",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
