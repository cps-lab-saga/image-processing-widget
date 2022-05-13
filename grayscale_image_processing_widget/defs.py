from pathlib import Path

try:
    from PySide6 import QtGui, QtWidgets, QtCore
    from PySide6.QtCore import Signal, Slot
except ModuleNotFoundError:
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot


def get_project_root() -> Path:
    return Path(__file__).parent
