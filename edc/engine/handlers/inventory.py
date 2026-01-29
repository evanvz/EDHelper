from __future__ import annotations
from typing import Any, Dict, List

def handle(engine, name: str | None, event: Dict[str, Any], msgs: List[str]) -> bool:
    """
    Inventory / commander state / load snapshots.
    Returns True if handled.
    """

    if name == "Commander":
        engine.state.commander = event.get("Name") or engine.state.commander
        engine.state.ship = event.get("Ship") or engine.state.ship
        engine.state.ship_id = event.get("ShipID") if isinstance(event.get("ShipID"), int) else engine.state.ship_id
        return True

    elif name == "LoadGame":
        # Some sessions emit this early; capture credits/ship basics if present.
        engine.state.commander = event.get("Commander") or engine.state.commander
        engine.state.ship = event.get("Ship") or engine.state.ship
        sid = event.get("ShipID")
        if isinstance(sid, int):
            engine.state.ship_id = sid
        return True

    elif name == "Materials":
        raw = event.get("Raw")
        manufactured = event.get("Manufactured")
        encoded = event.get("Encoded")
        if raw is not None:
            engine.state.materials_raw, engine.state.materials_raw_loc = engine._parse_materials_category(raw)
        if manufactured is not None:
            engine.state.materials_manufactured, engine.state.materials_manufactured_loc = engine._parse_materials_category(manufactured)
        if encoded is not None:
            engine.state.materials_encoded, engine.state.materials_encoded_loc = engine._parse_materials_category(encoded)
        return True

    elif name == "ShipLocker":
        # Odyssey storage
        locker = event.get("Items")
        if locker is not None:
            engine.state.shiplocker_items, engine.state.shiplocker_items_loc = engine._parse_shiplocker_items(locker)
        return True

    elif name == "ModuleBuy":
        # Lightweight ledger entry
        mod = event.get("BuyItem")
        if isinstance(mod, str) and mod.strip():
            msgs.append(f"Module bought: {mod}")
        return True

    elif name == "Cargo":
        # Cargo inventory snapshot
        inv = event.get("Inventory")
        if isinstance(inv, list):
            engine.state.cargo_inventory = inv
        return True

    return False