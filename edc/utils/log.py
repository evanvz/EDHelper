import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging(settings_dir: Path) -> None:
    settings_dir.mkdir(parents=True, exist_ok=True)
    log_file = settings_dir / "edc.log"

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,   # ~2 MB per file
        backupCount=3,        # keep 3 backups
        encoding="utf-8",
    )
    stream_handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            file_handler,
            stream_handler,
        ],
    )
