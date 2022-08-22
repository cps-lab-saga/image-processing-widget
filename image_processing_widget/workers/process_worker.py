from image_processing_widget.defs import QtCore, Signal


class ProcessWorker(QtCore.QObject):
    finished = Signal(object)

    def __init__(self, process, image, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.process = process
        self.image = image

    def run(self):
        processed_image = self.process(self.image)
        self.finished.emit(processed_image)
