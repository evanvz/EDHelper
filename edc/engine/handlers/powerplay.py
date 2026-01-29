from __future__ import annotations
from typing import Any, Dict, List

def handle(engine, name: str | None, event: Dict[str, Any], msgs: List[str]) -> bool:
    """
    Powerplay status events.
    Returns True if handled.
    """

    if name == "Powerplay":
        engine.state.power = event.get("Power") or engine.state.power
        engine.state.power_state = event.get("State") or engine.state.power_state

        merit = event.get("Merits")
        if isinstance(merit, int):
            engine.state.power_merits = merit

        rank = event.get("Rank")
        if isinstance(rank, int):
            engine.state.power_rank = rank

        # Optional messaging
        if engine.state.power:
            msgs.append(f"Powerplay: {engine.state.power} ({engine.state.power_state or 'n/a'})")
        return True

    return False