from image_processing_widget.defs import QtWidgets
from image_processing_widget.process_plugin import ProcessPlugin


class DoNothing(ProcessPlugin):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = DoNothing()
    widget.show()

    app.exec()
