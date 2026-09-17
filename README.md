# Zombie Sub 🧟💸

> **Zero-dependency, offline-first local bank statement auditor.**  
> Detect recurring leaks, zombie subscriptions, and silent rate hikes without uploading your financial data to fintech clouds or linking credentials to third-party aggregators.

---

## Why Zombie Sub?

Fintech apps and "subscription cancellers" demand full online banking credentials and siphon your complete transaction history to external data brokers. 

**Zombie Sub** runs 100% locally in your terminal. It parses standard exported transaction CSVs directly in RAM using Python's standard library. No Plaid, no API tokens, no cloud databases, and zero network calls.

### Core Features

* **Cadence Detection:** Flags monthly (~30-day) and annual recurring charges automatically.
* **Silent Rate Hike Alerts:** Compares historical charges to catch merchants quietly raising prices over time.
* **Annual Drag Calculation:** Projects total annualized cost for every recurring merchant descriptor.
* **Markdown Output:** Emits a clean, scannable Markdown table and action list.
* **Zero Dependencies:** Pure standard library. Runs anywhere Python 3 is installed.

---

## Quick Start

### 1. Download

**Windows (PowerShell):**
```powershell
curl.exe -fsSL [https://raw.githubusercontent.com/warknoc/zombie_sub/main/zombie_sub.py](https://raw.githubusercontent.com/warknoc/zombie_sub/main/zombie_sub.py) -o zombie_sub.py
