from queue import Queue

from image_processing_widget.defs import QtCore, Signal


class ProcessWorker(QtCore.QObject):
    finished = Signal(object)

    def __init__(self, dock, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dock = dock
        self.queue = Queue()

    def run(self):
        while True:
            img = self.queue.get()
            processed_image = self.process_img(img)
            self.finished.emit(processed_image)

    def process_img(self, img):
        process_widget = self.dock.process_groupbox.stacked_layout.currentWidget()
        oriented_image = self.dock.orient_groupbox.orient_img(img)
        return process_widget.process_img(oriented_image)
