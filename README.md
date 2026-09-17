# Zombie Sub 🧟💸

Zero-dependency, offline-first local bank statement auditor. Detect recurring leaks, zombie subscriptions, and silent rate hikes without uploading your financial data to fintech clouds or linking credentials to third-party aggregators.

---

## Why Zombie Sub?

Fintech apps and "subscription cancellers" demand full online banking credentials and siphon your complete transaction history to external data brokers. 

Zombie Sub runs 100% locally in your terminal. It parses standard exported transaction CSVs directly in RAM using Python's standard library. No Plaid, no API tokens, no cloud databases, and zero network calls.

### Core Features

* Cadence Detection: Flags monthly (~30-day) and annual recurring charges automatically.
* Silent Rate Hike Alerts: Compares historical charges to catch merchants quietly raising prices over time.
* Annual Drag Calculation: Projects total annualized cost for every recurring merchant descriptor.
* Markdown Output: Emits a clean, scannable Markdown table and action list.
* Zero Dependencies: Pure standard library. Runs anywhere Python 3 is installed.

---

## Quick Start

### 1. Download

Windows (PowerShell):
curl.exe -fsSL https://raw.githubusercontent.com/warknoc/zombie_sub/main/zombie_sub.py -o zombie_sub.py

macOS / Linux:
curl -fsSL https://raw.githubusercontent.com/warknoc/zombie_sub/main/zombie_sub.py -o zombie_sub.py

### 2. Export Statement

Download a transaction history CSV from your bank or credit card portal (typically available under Download Transactions or Export Activity).

### 3. Run the Audit

python zombie_sub.py your_statement.csv

---

## Sample Output

# Zombie Sub Audit: bank_statement.csv

Total Annualized Drain: $1,607.88 | Active Recurring Patterns: 3

| Merchant / Descriptor | Cadence | Latest Charge | Annualized Leak | Rate Hike | Last Billed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AWS CLOUD SERVICES** | Monthly | $64.00 | **$768.00** | +$15.00 | 2026-08-01 |
| **ADOBE CREATIVE CLOUD** | Monthly | $59.99 | **$719.88** | +$5.00 | 2026-08-20 |
| **GITHUB COPILOT SUB** | Monthly | $10.00 | **$120.00** | None | 2026-08-14 |

### Action Items
- Silent Creep Alert: AWS CLOUD SERVICES increased by $15.00 since first transaction.
- High Drag: AWS CLOUD SERVICES consumes $768.00/yr. Audit necessity.
- Silent Creep Alert: ADOBE CREATIVE CLOUD increased by $5.00 since first transaction.


---
**Support & Open Source Tip Rail**

Zombie_sub is open-source utility software licensed under MIT. If it saved you money:

USDC / Ethereum: 0x9805F8fd4A23Dd39cce11c03C10e6f966B1D6755

---

## Privacy Architecture

* Air-Gapped Execution: Does not import urllib, requests, socket, or any networking modules.
* Local In-Memory Processing: Data is evaluated in temporary memory and never written to an external store.
* No Telemetry: No analytics, logs, or usage tracking.

---

## License

MIT © 2026 warknoc
