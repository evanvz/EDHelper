import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import logging

log = logging.getLogger("edc.config")

def default_app_dir() -> Path:
    """
    Portable-in-repo runtime directory.
    Stores settings/logs under the project root so it moves with the folder:
    """
    start = Path(__file__).resolve().parent

    # Walk upwards until we find a "project root" marker.
    markers = ("main.py", "requirements.txt", "pyproject.toml", ".git", "ProjectStructure.txt")
    for p in (start, *start.parents):
        if any((p / m).exists() for m in markers):
            return p

    # Fallback: local to this file.
    return start

@dataclass
class AppConfig:
    journal_dir: Optional[str] = None
    # Exploration minimum value threshold in units of 100k credits.
    # Example: 1 => 100,000 cr; 10 => 1,000,000 cr; 100 => 10,000,000 cr
    min_planet_value_100k: int = 1
    exo_high_value_m: int = 2

class ConfigStore:
    def __init__(self, app_dir: Path):
        # app_dir == project root (portable-in-repo)
        self.app_dir = Path(app_dir)
        self.settings_dir = self.app_dir / "settings"
        self.path = self.settings_dir / "settings.json"
        # Back-compat: older layouts may have used <project_root>/settings.json
        self.legacy_path = self.app_dir / "settings.json"

    @property
    def settings_path(self) -> Path:
        return self.path

    def ensure_dirs(self) -> None:
        self.settings_dir.mkdir(parents=True, exist_ok=True)

    def _migrate_settings(self, data: dict, from_version: int) -> tuple[dict, bool]:
        """
        Returns: (migrated_data, changed)

        v1 -> v2:
          - normalize min_planet_value_100k
          - add schema_version
        """
        changed = False

        if from_version < 2:
            # Back-compat for older key variants.
            # NOTE: historical builds used a double-underscore key in some cases.
            if "min_planet_value_100k" not in data and "min_planet_value__100k" in data:
                try:
                    # Legacy stored in "millions" (or similar). Existing behavior multiplied by 10.
                    # Keep the same conversion to avoid breaking existing installs.
                    data["min_planet_value_100k"] = int(data.get("min_planet_value__100k") or 0) * 10
                except Exception:
                    data["min_planet_value_100k"] = 10
                changed = True

            if "schema_version" not in data or int(data.get("schema_version") or 1) != 2:
                data["schema_version"] = 2
                changed = True

        return data, changed

    def load(self) -> AppConfig:
        read_path = self.path
        if (not read_path.exists()) and self.legacy_path.exists():
            read_path = self.legacy_path

        if not read_path.exists():
            log.info(
                "No settings file found. Using defaults. app_dir=%s settings_dir=%s settings_path=%s",
                str(self.app_dir),
                str(self.settings_dir),
                str(self.path),
            )
            return AppConfig()
        try:
            data = json.loads(read_path.read_text(encoding="utf-8"))
            schema_version = int(data.get("schema_version", 1) or 1)
            migrated, changed = self._migrate_settings(data, schema_version)

            # If we loaded from legacy_path OR we migrated, write back to the canonical settings path.
            # This prevents "saved but not loaded" confusion between multiple settings.json locations.
            if changed or (read_path == self.legacy_path):
                try:
                    self.ensure_dirs()
                    self.path.write_text(json.dumps(migrated, indent=2), encoding="utf-8")
                    log.info("Migrated settings written to %s (loaded from %s)", str(self.path), str(read_path))
                    read_path = self.path
                    data = migrated
                except Exception:
                    log.exception("Failed to write migrated settings.json; continuing with in-memory settings only.")

            # New key: min_planet_value_100k (units of 100k credits)
            v100k = data.get("min_planet_value_100k", None)
            if isinstance(v100k, (int, float)):
                min_100k = int(v100k or 0)
            else:
                # If a weird type got stored, fall back safely.
                min_100k = 1

            if min_100k < 0:
                min_100k = 0

            log.info("Loaded settings from %s", str(read_path))
            return AppConfig(
                journal_dir=data.get("journal_dir"),
                min_planet_value_100k=min_100k,
                exo_high_value_m=int(data.get("exo_high_value_m", 2) or 2),
            )

        except Exception:
            log.exception("Failed to load settings.json, using defaults.")
            return AppConfig()

    def save(self, cfg: AppConfig) -> None:
        try:
            self.ensure_dirs()
            self.path.write_text(
                json.dumps(
                    {
                        "schema_version": SCHEMA_VERSION,
                        "journal_dir": cfg.journal_dir,
                        # New storage (100k units)
                        "min_planet_value_100k": int(getattr(cfg, "min_planet_value_100k", 1) or 1),
                        # Legacy storage (1M units) for older builds/config readers
                        "exo_high_value_m": int(getattr(cfg, "exo_high_value_m", 2) or 2),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            log.info("Saved settings to %s", str(self.path))
        except Exception:
            log.exception("Failed to save settings.json")
