import logging
import sys
from configparser import ConfigParser
from pathlib import Path

import cv2 as cv
import qtawesome as qta

from image_processing_widget.custom_components import tab10_qcolor
from image_processing_widget.defs import (
    QtCore,
    QtWidgets,
    QtGui,
    project_root,
    settings_file,
    log_file,
    ReadMode,
)
from image_processing_widget.display_widget.image_widget import ImageWidget
from image_processing_widget.dock import Dock
from image_processing_widget.funcs import check_file_type, imread, imwrite
from image_processing_widget.workers import ProcessWorker


class MainWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_logger()
        self.log_new_session()

        self.setWindowTitle("Image Processing")
        self.resize(1000, 500)
        self.setAcceptDrops(True)
        self.setWindowIcon(
            QtGui.QIcon(qta.icon("fa5s.images", color=tab10_qcolor["blue"]))
        )

        self.project_paths = [project_root(), Path.cwd(), project_root().parent]
        logging.info(
            f"Looking for config file in {*[str(x) for x in self.project_paths],}."
        )
        self.config_parser = self.read_config()

        self.read_mode = self.get_read_mode(self.config_parser)

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)

        self.img_path = None
        self.original_img = None
        self.processed_img = None

        self.dock = Dock()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock)

        self.img_widget = ImageWidget()
        self.main_layout.addWidget(self.img_widget)

        self.process_thread = QtCore.QThread()
        self.process_worker = ProcessWorker(self.dock)
        self.process_worker.moveToThread(self.process_thread)
        self.process_worker.finished.connect(self.finished_process_image)
        self.process_thread.started.connect(self.process_worker.run)
        self.process_thread.start()

        self.connect_ui()

        # load settings from previous session
        self.settings_file = settings_file()
        if self.settings_file.is_file():
            settings = QtCore.QSettings(
                str(self.settings_file), QtCore.QSettings.IniFormat
            )
            self.gui_restore(settings)

        self.img_widget.setFocus()

    def read_config(self):
        parser = ConfigParser()
        for p in self.project_paths:
            config_file = p / "image_processing_config.ini"
            if config_file.is_file():
                parser.read(config_file)
                logging.info(f"Config file found: {config_file}")
                return parser

        logging.warning("Config file not found")
        return parser

    @staticmethod
    def get_read_mode(config_parser):
        if config_parser is None or not config_parser.has_option(
            "Image Config", "read_mode"
        ):
            logging.warning("Using default read_mode: COLOR")
            return ReadMode.COLOR

        read_mode = config_parser.get("Image Config", "read_mode").strip()
        if read_mode.upper() == "COLOR":
            logging.info(f"Read_mode: {read_mode}")
            return ReadMode.COLOR
        elif read_mode.upper() == "GRAYSCALE":
            logging.info(f"Read_mode: {read_mode}")
            return ReadMode.GRAYSCALE
        else:
            logging.warning(f"Invalid read_mode: {read_mode}")
            logging.warning("Using default read_mode: COLOR")
            return ReadMode.COLOR

    def connect_ui(self):
        self.dock.connect_ui(self.start_process_image)
        self.dock.peek_groupbox.peek_button.pressed.connect(self.peek_original_img)
        self.dock.peek_groupbox.peek_button.released.connect(self.show_processed_image)
        self.dock.save_groupbox.save_button.clicked.connect(self.save_button_clicked)
        self.dock.save_groupbox.save_as_button.clicked.connect(
            self.save_as_button_clicked
        )

    def finished_process_image(self, processed_image):
        self.processed_img = processed_image
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.show_processed_image()

    def start_process_image(self):
        if self.img_path:
            q = self.process_worker.queue
            with q.mutex:
                q.queue.clear()
            q.put(self.original_img)
            self.setCursor(QtCore.Qt.BusyCursor)

    def peek_original_img(self):
        oriented_image = self.dock.orient_groupbox.orient_img(self.original_img)
        self.img_widget.setImage(oriented_image)

    def show_processed_image(self):
        self.img_widget.setImage(self.processed_img)

    def read_img(self, path):
        self.img_path = path
        if self.read_mode == ReadMode.GRAYSCALE:
            self.original_img = imread(self.img_path, cv.IMREAD_GRAYSCALE)
        elif self.read_mode == ReadMode.COLOR:
            self.original_img = imread(self.img_path, cv.IMREAD_COLOR)
            self.original_img = cv.cvtColor(self.original_img, cv.COLOR_BGR2RGB)

        self.start_process_image()
        self.dock.process_groupbox.adjust_range(self.original_img.shape)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            path = Path(e.mimeData().urls()[0].toLocalFile())
            if check_file_type(path, "image"):
                e.acceptProposedAction()
                e.setDropAction(QtCore.Qt.LinkAction)
        else:
            super().dragEnterEvent(e)

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            path = Path(e.mimeData().urls()[0].toLocalFile())
            if check_file_type(path, "image"):
                e.setDropAction(QtCore.Qt.LinkAction)
                e.accept()
        else:
            super().dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.setDropAction(QtCore.Qt.LinkAction)
            path = Path(e.mimeData().urls()[0].toLocalFile())
            if check_file_type(path, "image"):
                e.accept()
                self.read_img(path)
        else:
            super().dropEvent(e)

    def gui_save(self, settings):
        self.dock.gui_save(settings)
        settings.setValue("Window/geometry", self.saveGeometry())
        settings.setValue("Window/state", self.saveState())

    def gui_restore(self, settings):
        if geometry := settings.value("Window/geometry"):
            self.restoreGeometry(geometry)
        if state := settings.value("Window/state"):
            self.restoreState(state)
        self.dock.gui_restore(settings)

    def closeEvent(self, event):
        """save before closing"""
        settings = QtCore.QSettings(str(self.settings_file), QtCore.QSettings.IniFormat)
        self.gui_save(settings)
        event.accept()

    def error_dialog(self, error):
        QtWidgets.QMessageBox.critical(self, "Error", error)

    def save_as_button_clicked(self):
        if self.img_path:
            save_url, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save As", str(self.img_path)
            )
            if save_url:
                save_path = Path(save_url)
                if self.processed_img is not None:
                    self.save_image(save_path, self.processed_img)

    def save_button_clicked(self):
        if self.img_path:
            reply = QtWidgets.QMessageBox.warning(
                self,
                "Confirm Save",
                f"{self.img_path.name} already exists.\n" f"Do you want to replace it?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            if reply == QtWidgets.QMessageBox.Yes and self.processed_img is not None:
                self.save_image(self.img_path, self.processed_img)

    def save_image(self, save_path, img):
        try:
            imwrite(save_path, img)
        except Exception as e:
            self.error_dialog(e.err)
        else:
            self.ask_load_saved(save_path)

    def ask_load_saved(self, save_path):
        if self.img_path:
            reply = QtWidgets.QMessageBox.warning(
                self,
                "Load Saved",
                "Do you want to load the saved file?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )

            if reply == QtWidgets.QMessageBox.Yes:
                self.read_img(save_path)

    @staticmethod
    def setup_logger():
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

        log_handler_stdout = logging.StreamHandler(sys.stdout)
        log_handler_stdout.setFormatter(formatter)

        log_handler_file = logging.FileHandler(log_file())
        log_handler_file.setFormatter(formatter)

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        log.addHandler(log_handler_stdout)
        log.addHandler(log_handler_file)

    @staticmethod
    def log_new_session():
        banner = "-" * 20 + " New Session " + "-" * 20
        logging.info("")
        logging.info("=" * len(banner))
        logging.info(banner)
        logging.info("=" * len(banner))


def main():
    app = QtWidgets.QApplication([])
    win = MainWidget()
    win.show()

    app.exec()


if __name__ == "__main__":
    main()
