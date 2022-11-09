import logging
from queue import Queue

from image_processing_widget.defs import QtCore, Signal


class ProcessWorker(QtCore.QObject):
    finished = Signal(object)
    process_failed = Signal(str)

    def __init__(self, dock, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dock = dock
        self.queue = Queue()

        self._stop_flag = False

    def run(self):
        while not self._stop_flag:
            img = self.queue.get()
            if img is not None:
                processed_image = self.process_img(img)
                self.finished.emit(processed_image)

    def process_img(self, img):
        process_widget = self.dock.process_groupbox.stacked_layout.currentWidget()
        try:
            oriented_image = self.dock.orient_groupbox.orient_img(img)
            return process_widget.process_img(oriented_image)
        except Exception as e:
            logging.error(f"{process_widget.name}: {e}")
            self.process_failed.emit(f"{e}")
            return

    def stop(self):
        self._stop_flag = True
        self.queue.put(None)
