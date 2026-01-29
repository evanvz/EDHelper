import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger("edc.external_intel")

class ExternalIntel:
    """
    Offline, advisory-only POI store.

    File location (portable-in-repo):
      <settings_dir>/external_pois.json
    """

    def __init__(self, settings_dir: Path, filename: str = "external_pois.json"):
        self.path = Path(settings_dir) / filename
        self._mtime: Optional[float] = None
        self._systems: Dict[str, List[Dict[str, Any]]] = {}
        self._addresses: Dict[str, List[Dict[str, Any]]] = {}
        self._load(force=True)

    def _load(self, force: bool = False) -> None:
        try:
            if not self.path.exists():
                self._systems = {}
                self._addresses = {}
                self._mtime = None
                return

            m = self.path.stat().st_mtime
            if (not force) and (self._mtime is not None) and (m == self._mtime):
                return

            data = json.loads(self.path.read_text(encoding="utf-8"))
            self._mtime = m

            systems = {}
            addrs = {}
            if isinstance(data, dict):
                systems = data.get("systems") or {}
                addrs = data.get("system_addresses") or {}

            self._systems = systems if isinstance(systems, dict) else {}
            self._addresses = addrs if isinstance(addrs, dict) else {}
        except Exception:
            log.exception("Failed to load external_pois.json")
            self._systems = {}
            self._addresses = {}
            self._mtime = None

    def get_pois(self, system_name: str, system_address: Optional[int] = None) -> List[Dict[str, Any]]:
        # Reload if the file changed
        self._load(force=False)

        out: List[Dict[str, Any]] = []
        try:
            if isinstance(system_address, int):
                recs = self._addresses.get(str(system_address)) or []
                if isinstance(recs, list):
                    out.extend([r for r in recs if isinstance(r, dict)])

            recs2 = self._systems.get(system_name) or []
            if isinstance(recs2, list):
                out.extend([r for r in recs2 if isinstance(r, dict)])
        except Exception:
            pass

        return out
