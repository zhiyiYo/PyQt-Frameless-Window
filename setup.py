import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PySideSix-Frameless-Window",
    version="0.3.1",
    keywords="pyside6 frameless",
    author="zhiyiYo",
    author_email="shokokawaii@outlook.com",
    description="A cross-platform frameless window based on pyside6, support Win32, Linux and macOS.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="LGPLv3",
    url="https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6",
    packages=setuptools.find_packages(),
    install_requires=[
        "pywin32;platform_system=='Windows'",
        "pyobjc;platform_system=='Darwin'",
        "PyCocoa;platform_system=='Darwin'",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent'
    ]
)
