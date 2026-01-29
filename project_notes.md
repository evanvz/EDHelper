# Elite Dangerous Companion (EDC) — Project Notes

> **Status:** Living document (authoritative)
>
> **Purpose:** Capture the intent, architecture, rules, and future direction of the EDC project.
>
> **Dependency:** This project inherits rules from **AI_HUMAN_CONTRACT.md**. That contract must be read first.

---

## 1. Project Overview

### 1.1 What this project is

EDC is an **offline-first, journal-driven companion application** for *Elite Dangerous*.

Its purpose is to:
- React to **live journal events** in real time
- Provide **decision support**, not automation
- Reduce player cognitive load by surfacing **what matters now**

The journal is the **single source of truth**.

### 1.2 What this project is NOT

- Not an autopilot
- Not a route planner
- Not a background polling service
- Not a replacement for the game UI

The app **never issues commands** and **never alters gameplay**.

---

## 2. Core Design Philosophy

1. **Journal-first**  
   All logic must be derived from journal events. External data is advisory only.

2. **Low noise**  
   Only surface information that changes player decisions.

3. **Clear domain separation**  
   HUD ≠ Overview ≠ Tabs

4. **Small, safe changes**  
   One patch, one purpose.

5. **Observable before implemented**  
   If behavior is unclear, capture journal data first.

---

## 3. Runtime Architecture

### 3.1 Data flow

```
Journal → JournalWatcher → EventEngine → GameState → UI refresh
```

- **JournalWatcher**
  - Tails the latest journal file
  - Emits raw events via Qt signals

- **EventEngine**
  - Interprets journal events
  - Mutates GameState
  - Never touches UI directly

- **GameState**
  - Single source of truth for UI
  - Holds *current system* and *session state*

- **UI (MainWindow)**
  - Reads from GameState only
  - Never mutates state

---

## 4. UI Model & Responsibilities

### 4.1 HUD — Immediate Awareness

- No history
- No tables
- No scrolling
- No action lists

If it requires thinking, it does **not** belong in HUD.

---

### 4.2 Overview — What Matters *Now*

- Action hints only
- Clickable links to tabs
- No deep data

Overview must never duplicate tab content.

---

### 4.3 Tabs = Domain Memory

Each tab owns **one domain** and keeps *per-system memory*.

#### Exploration
- High-value planets only
- FSS vs DSS logic
- Slider represents **confirmed (DSS) value**

#### Exobiology
- FSS: BioSignals → placeholder targets
- DSS: Genus revealed
- ScanOrganic: Species + progress

#### Combat
- Contacts scanned at ScanStage ≥ 3
- Per-system memory
- Dedupe logic
- Current target highlighting

#### PowerPlay
- Journal-derived only
- No external polling
- Advisory actions only

---

## 5. Configuration & Persistence

### 5.1 What is persisted

- Journal directory
- Exploration high-value threshold
- Exobiology high-value threshold

### 5.2 What is NOT persisted

- Per-system contacts
- Per-system PP actions
- Temporary alerts

These reset naturally on system change.

---

## 6. Update & Patch Rules (Project-Specific)

> These rules apply **in addition to** the AI–Human Contract.

### 6.1 Local-diff format ONLY

Every patch must:
- Start with `*** file: <path>`
- Include `@@` hunk markers
- Show context lines
- Use `-` for removals, `+` for additions

Patches are applied manually in **Windows Notepad**.

---

### 6.2 One purpose per patch

Exactly one intent per patch.

---

### 6.3 Never guess journal fields

If unsure:
1. Capture real journal snippet
2. Observe
3. Implement

---

### 6.4 Indentation safety

- Keep hunks small
- Avoid moving large blocks
- Prefer additive changes

---

### 6.5 Enviroment

- App is running on a Windows PC inside a Python venv

- review ProjectStructure.txt for app structure.

---

## 7. Future Domains (Planned)

### Mining
- Separate tab
- Ring types & hotspots
- NOT part of Overview

### Engineering & Materials
- Blueprint-driven
- Track **have vs need**
- No auto-planning

### Trading
- Separate domain
- Journal-first

---

## 8. Database (Future)

Purpose:
- Historical memory
- Revisit awareness
- Personal scan history

Rules:
- Journal always wins
- DB is advisory

---

## 9. Visual Direction (Future)

- Elite-style color language
- Semantic colors
- Icons over text
- Reactive emphasis

Polish comes **after** functional stability.

---

## 10. Final Note

Any change that violates these principles should be questioned before implementation.

---

## 11. Session Start Block (MANDATORY)

This project is often worked on across **multiple chat sessions**.
A new chat session resets all active AI constraints unless they are explicitly re-activated.

Therefore, at the start of **every new chat**, the human must activate the working rules for this project.

### Preferred activation (short and explicit)

> **"Project Notes are authoritative. Restricted Execution Mode. Local-diff patches only. If unsure, stop and ask."**

### Strict activation (recommended for patch work)

> **"This session is governed by project_notes.md. Local-diff format only. Hard-Stop Protocol applies."**

### Verification-required (safest)

> **"Do not proceed until you confirm Restricted Execution Mode is active."**

---

## 12. AI Acknowledgement Requirement

Upon session start, the AI **must explicitly acknowledge** activation by responding with:

> **"Acknowledged. Restricted Execution Mode active. project_notes.md loaded."**

If this acknowledgement does not occur, **the session must stop immediately**.

---

## 13. Failure Handling

If the AI:
- Proceeds without acknowledging the rules
- Produces output that violates the local-diff format
- Assumes context without asking for clarification

Then the correct response is:

> **"Contract violation. Stop."**

No further work should continue until the session is reset and re-activated.

