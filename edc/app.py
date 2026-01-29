from PyQt6.QtWidgets import QApplication
from pathlib import Path
import logging

from edc.config import ConfigStore, default_app_dir
from edc.utils.log import setup_logging
from edc.ui.main_window import MainWindow

def run():
    base_dir = default_app_dir()          # project root
    cfg_store = ConfigStore(base_dir)     # exposes cfg_store.settings_dir
    setup_logging(cfg_store.settings_dir) # logs live under <project_root>/settings

    log = logging.getLogger("edc.app")
    log.info("Startup paths: app_dir=%s settings_dir=%s settings_path=%s",
             str(cfg_store.app_dir), str(cfg_store.settings_dir), str(cfg_store.settings_path))

    cfg = cfg_store.load()

    app = QApplication([])
    win = MainWindow(cfg_store, cfg)
    win.show()
    app.exec()
