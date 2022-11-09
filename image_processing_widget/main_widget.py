import logging
import sys
from configparser import ConfigParser
from pathlib import Path
from time import sleep

import cv2 as cv
from yapsy.PluginManager import PluginManager

from image_processing_widget.defs import (
    QtCore,
    QtWidgets,
    QtGui,
    project_root,
    settings_file,
    resource_dir,
    log_file,
)
from image_processing_widget.display_widget.image_widget import ImageWidget
from image_processing_widget.docks import ControlsDock
from image_processing_widget.funcs import check_file_type, imread, imwrite
from image_processing_widget.process_plugin import ProcessPlugin
from image_processing_widget.roi_plugin import RoiPlugin
from image_processing_widget.splashscreen import SplashScreen
from image_processing_widget.workers import ProcessWorker


class MainWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.splashscreen = SplashScreen()
        self.splashscreen.show()
        self.setup_logger()
        self.log_new_session()

        self.setWindowTitle("Image Processing")
        self.resize(1000, 500)
        self.setAcceptDrops(True)
        self.setWindowIcon(QtGui.QIcon(str(resource_dir() / "camera.svg")))

        self.project_paths = [project_root(), Path.cwd(), project_root().parent]
        logging.info(
            f"Looking for config file in {', '.join([str(x) for x in self.project_paths])}."
        )
        self.config_parser = self.read_config()

        self.selected_process_plugins = self.get_plugins(
            self.config_parser, "process_plugins"
        )
        self.selected_roi_plugins = self.get_plugins(self.config_parser, "roi_plugins")
        logging.info(f"Process plugins {self.selected_process_plugins} were selected.")
        logging.info(f"ROI plugins {self.selected_roi_plugins} were selected.")
        self.plugin_dirs = [x / "plugins" for x in self.project_paths]

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)

        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        self.splashscreen.set_progress(10)

        self.img_path = None
        self.original_img = None
        self.processed_img = None

        self.controls_dock = ControlsDock()
        self.controls_dock.mode_changed.connect(lambda: self.read_img(None))
        self.controls_dock.settings_updated.connect(self.start_process_image)
        self.controls_dock.peek_started.connect(self.peek_original_img)
        self.controls_dock.peek_ended.connect(self.show_processed_image)
        self.controls_dock.save.connect(self.save_button_clicked)
        self.controls_dock.save_as.connect(self.save_as_button_clicked)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.controls_dock)

        self.img_widget = ImageWidget(self.config_parser)
        self.main_layout.addWidget(self.img_widget)
        self.img_widget.slice_selected.connect(self.roi_shown)
        self.img_widget.slice_selection_changed.connect(self.roi_moved)

        self.plugin_docks = {}
        self.process_plugins = {}
        self.roi_plugins = {}
        self.plugin_manager = PluginManager(
            categories_filter={"ProcessPlugin": ProcessPlugin, "RoiPlugin": RoiPlugin},
            plugin_info_ext="image-processing-plugin",
            directories_list=self.plugin_dirs,
        )
        self.plugin_manager.locatePlugins()
        self.plugin_manager.loadPlugins()
        self.setup_process_plugins(self.plugin_manager, self.selected_process_plugins)
        self.setup_roi_plugins(self.plugin_manager, self.selected_roi_plugins)

        self.splashscreen.set_progress(50)

        self.process_thread = QtCore.QThread()
        self.process_worker = ProcessWorker(self.controls_dock)
        self.process_worker.moveToThread(self.process_thread)
        self.process_worker.finished.connect(self.finished_process_image)
        self.process_worker.process_failed.connect(self.error_dialog)
        self.process_thread.started.connect(self.process_worker.run)
        self.process_thread.start()

        # load settings from previous session
        self.settings_file = settings_file()
        if self.settings_file.is_file():
            settings = QtCore.QSettings(
                str(self.settings_file), QtCore.QSettings.IniFormat
            )
            self.gui_restore(settings)
            logging.info(f"Restoring GUI from {str(self.settings_file)}.")

        self.img_widget.setFocus()

        self.splashscreen.set_progress(80)
        self.splashscreen.finish(self)

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
    def get_plugins(config_parser, key):
        if config_parser.has_option("Plugins", key):
            return [
                x.strip() for x in config_parser.get("Plugins", key).split(",") if x
            ]
        else:
            return []

    def setup_process_plugins(self, plugin_manager, selected_plugins):
        available_plugins = {
            plugin_info.name: plugin_info
            for plugin_info in plugin_manager.getPluginsOfCategory("ProcessPlugin")
        }

        if missing_plugins := (set(selected_plugins) - set(available_plugins)):
            msg = f"Selected process plugins [{', '.join(missing_plugins)}] are not available"
            self.error_dialog(msg)
            logging.warning(msg)

        for plugin_info in available_plugins.values():
            if (
                plugin_info.name in selected_plugins
                and plugin_info.name not in self.process_plugins.keys()
            ):
                self.activate_process_plugin(plugin_info)

    def setup_roi_plugins(self, plugin_manager, selected_plugins):
        available_plugins = {
            plugin_info.name: plugin_info
            for plugin_info in plugin_manager.getPluginsOfCategory("RoiPlugin")
        }

        if missing_plugins := (set(selected_plugins) - set(available_plugins)):
            msg = (
                f"Selected roi plugins [{', '.join(missing_plugins)}] are not available"
            )
            self.error_dialog(msg)
            logging.warning(msg)

        for plugin_info in available_plugins.values():
            if (
                plugin_info.name in selected_plugins
                and plugin_info.name not in self.roi_plugins.keys()
            ):
                self.activate_roi_plugin(plugin_info)

    def activate_process_plugin(self, plugin_info):
        self.controls_dock.process_groupbox.add_process_plugin(
            plugin_info.name, plugin_info.plugin_object
        )
        plugin_info.plugin_object.process_failed.connect(self.error_dialog)
        self.process_plugins[plugin_info.name] = plugin_info.plugin_object
        logging.info(f"Added process plugin: {plugin_info.name}.")

    def activate_roi_plugin(self, plugin_info):
        if plugin_info.plugin_object.dock is not None:
            self.plugin_docks[plugin_info.name] = plugin_info.plugin_object.dock
            self.addDockWidget(
                QtCore.Qt.RightDockWidgetArea,
                self.plugin_docks[plugin_info.name],
            )
        self.roi_plugins[plugin_info.name] = plugin_info.plugin_object
        logging.info(f"Added roi plugin: {plugin_info.name}.")

    def finished_process_image(self, processed_image):
        if processed_image is None:
            self.setCursor(QtCore.Qt.ArrowCursor)
            return

        self.processed_img = processed_image
        self.show_processed_image()
        self.setCursor(QtCore.Qt.ArrowCursor)

    def start_process_image(self):
        if self.original_img is not None:
            q = self.process_worker.queue
            with q.mutex:
                q.queue.clear()
            q.put(self.original_img)
            self.setCursor(QtCore.Qt.BusyCursor)

    def peek_original_img(self):
        oriented_image = self.controls_dock.orient_groupbox.orient_img(
            self.original_img
        )
        self.img_widget.set_image(oriented_image)

    def show_processed_image(self):
        self.img_widget.set_image(self.processed_img)

    def read_img(self, path):
        if path is not None:
            self.img_path = path
        if self.img_path is None:
            return

        try:
            if self.controls_dock.image_mode_groupbox.mode == "grayscale":
                self.original_img = imread(self.img_path, cv.IMREAD_GRAYSCALE)
            elif self.controls_dock.image_mode_groupbox.mode == "color":
                self.original_img = imread(self.img_path, cv.IMREAD_COLOR)
                self.original_img = cv.cvtColor(self.original_img, cv.COLOR_BGR2RGB)
            else:
                raise ValueError("Invalid read mode.")
            self.controls_dock.process_groupbox.adjust_range(self.original_img.shape)
        except ValueError as e:
            self.error_dialog(str(e))

        self.start_process_image()

    def roi_shown(self, show):
        for plugin in self.roi_plugins.values():
            plugin.roi_shown(show)

    def roi_moved(self, img_slice):
        for plugin in self.roi_plugins.values():
            plugin.roi_moved(img_slice)

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
        self.controls_dock.gui_save(settings)
        settings.setValue("Window/geometry", self.saveGeometry())
        settings.setValue("Window/state", self.saveState())

    def gui_restore(self, settings):
        try:
            if geometry := settings.value("Window/geometry"):
                self.restoreGeometry(geometry)
            if state := settings.value("Window/state"):
                self.restoreState(state)
            self.controls_dock.gui_restore(settings)
        except Exception as e:
            self.error_dialog(f"{self.settings_file} is corrupted!\n{str(e)}")
            logging.warning(f"{self.settings_file} is corrupted!")

    def closeEvent(self, event):
        """save before closing"""
        self.process_worker.stop()
        self.process_thread.quit()
        settings = QtCore.QSettings(str(self.settings_file), QtCore.QSettings.IniFormat)
        self.gui_save(settings)
        while self.process_thread.isRunning():
            sleep(0.5)
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
            self.error_dialog(str(e))
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
