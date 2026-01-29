# EDHelper (Elite Dangerous Helper)

EDHelper is a desktop companion application for *Elite Dangerous* that reads the live Frontier Journal files and presents contextual, actionable information to the player while in-game.

The project focuses on **real-time situational awareness**, not automation, and does not read game memory or interfere with the game client.

---

## Core Purpose

EDHelper monitors Elite Dangerous journal events and provides:

- System overview information (government, economy, security, population)
- Exploration intelligence (high-value bodies, scan status)
- Exobiology tracking and valuation
- PowerPlay context and advisory actions
- Inventory and material awareness
- External points-of-interest and farming hints (optional)

All information is derived **exclusively from journal events and static reference data**.

---

## High-Level Architecture

- **Journal Watcher**
  - Monitors Frontier journal files in real time
  - Dispatches events as they are written by the game

- **Event Engine**
  - Processes journal events
  - Updates a single authoritative game state

- **Core State**
  - Central, in-memory representation of the current commander/system context

- **Handlers**
  - Event-specific logic (exploration, exobiology, inventory, powerplay, etc.)

- **UI Layer**
  - Renders state and advisory output
  - No direct game logic or journal parsing

---

## Design Principles

- Journal-only data (no memory reading)
- Clear separation between logic and UI
- Deterministic, explainable outputs
- Safe to run alongside the game
- No automation or gameplay control

---

## Status

This project is under **active development** and is evolving iteratively.
Structure and behavior may change as features mature.

