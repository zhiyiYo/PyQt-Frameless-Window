import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PySide2-Frameless-Window",
    version="0.0.3",
    keywords="pyside2 frameless",
    author="zhiyiYo",
    author_email="shokokawaii@outlook.com",
    description="A cross-platform frameless window based on pyside2, support Win32, Linux and macOS.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/Pyside2",
    packages=setuptools.find_packages(),
    install_requires=[
        "pywin32;platform_system=='Windows'",
        "pyobjc;platform_system=='Darwin'",
        "PyCocoa;platform_system=='Darwin'",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
