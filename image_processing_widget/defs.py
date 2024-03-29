import importlib.metadata
import os
from enum import Enum, auto
from pathlib import Path
from sys import platform

__version__ = importlib.metadata.version("image_processing_widget")

try:
    from PySide6 import QtGui, QtWidgets, QtCore
    from PySide6.QtCore import Signal, Slot

    backend_name = "pyside6"

except ModuleNotFoundError:
    try:
        from PyQt6 import QtGui, QtWidgets, QtCore
        from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

        backend_name = "pyqt6"

    except ModuleNotFoundError:
        from PyQt5 import QtGui, QtWidgets, QtCore
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

        backend_name = "pyqt5"

if platform == "linux" or platform == "linux2":
    os.environ["QT_QPA_PLATFORM"] = "xcb"


def project_root() -> Path:
    Path(__file__).parent.mkdir(exist_ok=True, parents=True)
    return Path(__file__).parent


def settings_file() -> Path:
    p = project_root()
    if "Temp" in p.parts:
        f = (
            p.parents[len(p.parts) - 2 - p.parts.index("Temp")]
            / "image_processing"
            / "image_processing_restore.ini"
        )
    else:
        f = project_root() / "image_processing_restore.ini"

    f.parent.mkdir(exist_ok=True, parents=True)
    return f


def log_file() -> Path:
    return Path.cwd() / "image_processing.log"


def resource_dir() -> Path:
    return project_root() / "resource"


class DisplayMode(Enum):
    AUTO = auto()
    BIT8 = auto()
