import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PyQt6-Frameless-Window",
    version="0.3.8",
    keywords="pyqt6 frameless",
    author="zhiyiYo",
    author_email="shokokawaii@outlook.com",
    description="A cross-platform frameless window based on pyqt6, support Win32, Linux and macOS.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPLv3",
    url="https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PyQt6",
    packages=setuptools.find_packages(),
    install_requires=[
        "pywin32;platform_system=='Windows'",
        "pyobjc;platform_system=='Darwin'",
        "PyCocoa;platform_system=='Darwin'",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ]
)
