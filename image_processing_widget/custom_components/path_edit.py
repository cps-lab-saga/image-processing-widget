from pathlib import Path

from image_processing_widget.defs import QtCore, QtWidgets


class PathEdit(QtWidgets.QLineEdit):
    def __init__(self, mode="directory", parent=None):
        super().__init__(parent=parent)

        self.setAcceptDrops(True)
        self.mode = mode

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            e.setDropAction(QtCore.Qt.LinkAction)
        else:
            super().dragEnterEvent(e)

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.setDropAction(QtCore.Qt.LinkAction)
            e.accept()
        else:
            super().dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.setDropAction(QtCore.Qt.LinkAction)
            e.accept()
            for url in e.mimeData().urls():
                path = Path(url.toLocalFile())
                if (self.mode == "directory" and path.is_dir()) or (
                    self.mode == "file" and path.is_file()
                ):
                    self.setText(str(path.resolve()))
        else:
            super().dropEvent(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = PathEdit()
    widget.show()

    app.exec()
