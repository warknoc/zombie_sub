#!/usr/bin/env python3
"""
ZOMBIE_SUB: Local Bank Statement & Recurring Charge Auditor
Zero-dependency, offline-first Python script to detect recurring leaks,
zombie subscriptions, and silent rate hikes from transaction exports.
"""

import sys
import os
import csv
import re
from collections import defaultdict
from datetime import datetime

DATE_FORMATS = [
    "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", 
    "%m-%d-%Y", "%Y/%m/%d", "%b %d, %Y", "%d-%b-%Y"
]

def clean_amount(val):
    if not val:
        return 0.0
    val = val.replace("$", "").replace(",", "").strip()
    if val.startswith("(") and val.endswith(")"):
        val = f"-{val[1:-1]}"
    try:
        return abs(float(val))
    except ValueError:
        return 0.0

def parse_date(val):
    val = val.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(val, fmt)
        except ValueError:
            continue
    return None

def normalize_merchant(desc):
    desc = desc.upper()
    desc = re.sub(r'#\S+', '', desc)
    desc = re.sub(r'\*+', ' ', desc)
    desc = re.sub(r'\d{4,}', '', desc)
    desc = re.sub(r'\b(PURCHASE|RECURRING|AUTO-DEBIT|DEBIT|ACH|CHECK|POS|PAYMENT|ONLINE)\b', '', desc)
    desc = re.sub(r'[^A-Z0-9\s]', ' ', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    tokens = desc.split()
    return " ".join(tokens[:4]) if tokens else "UNKNOWN_MERCHANT"

def analyze_statement(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' not found.", file=sys.stderr)
        sys.exit(1)

    transactions = defaultdict(list)

    with open(csv_path, mode="r", encoding="utf-8-sig", errors="replace") as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
            reader = csv.reader(f, dialect)
        except Exception:
            reader = csv.reader(f)

        header = [col.strip().lower() for col in next(reader, [])]

        date_idx, desc_idx, amt_idx = -1, -1, -1
        for i, col in enumerate(header):
            if any(k in col for k in ["date", "trans_date", "posted"]):
                date_idx = i
            elif any(k in col for k in ["desc", "merchant", "name", "payee", "memo"]):
                desc_idx = i
            elif any(k in col for k in ["amount", "amt", "debit", "charge"]):
                amt_idx = i

        if min(date_idx, desc_idx, amt_idx) == -1:
            print("Error: Could not auto-detect Date, Description, and Amount columns.", file=sys.stderr)
            sys.exit(1)

        for row in reader:
            if len(row) <= max(date_idx, desc_idx, amt_idx):
                continue
            dt = parse_date(row[date_idx])
            amt = clean_amount(row[amt_idx])
            raw_desc = row[desc_idx]
            merchant = normalize_merchant(raw_desc)

            if dt and amt > 0:
                transactions[merchant].append({
                    "date": dt,
                    "amount": amt,
                    "raw": raw_desc
                })

    recurring = []
    for merchant, records in transactions.items():
        if len(records) >= 2:
            records.sort(key=lambda x: x["date"])
            intervals = [(records[i]["date"] - records[i-1]["date"]).days for i in range(1, len(records))]
            avg_interval = sum(intervals) / len(intervals)

            is_monthly = any(25 <= iv <= 35 for iv in intervals) or (25 <= avg_interval <= 35)
            is_annual = any(350 <= iv <= 375 for iv in intervals)

            if is_monthly or is_annual:
                cadence = "Monthly" if is_monthly else "Annual"
                amounts = [r["amount"] for r in records]
                base_amt = amounts[0]
                latest_amt = amounts[-1]
                price_creep = latest_amt > base_amt
                creep_diff = latest_amt - base_amt if price_creep else 0.0
                annual_drain = latest_amt * 12 if is_monthly else latest_amt

                recurring.append({
                    "merchant": merchant,
                    "cadence": cadence,
                    "hits": len(records),
                    "latest_cost": latest_amt,
                    "annual_drain": annual_drain,
                    "price_creep": price_creep,
                    "creep_diff": creep_diff,
                    "last_billed": records[-1]["date"].strftime("%Y-%m-%d")
                })

    recurring.sort(key=lambda x: x["annual_drain"], reverse=True)
    total_annual = sum(r["annual_drain"] for r in recurring)

    print(f"# Zombie Sub Audit: `{os.path.basename(csv_path)}`\n")
    print(f"**Total Annualized Drain:** `${total_annual:,.2f}` | **Active Recurring Patterns:** `{len(recurring)}`\n")

    if not recurring:
        print("> **No recurring charges or subscription cadences identified.**")
        return

    print("| Merchant / Descriptor | Cadence | Latest Charge | Annualized Leak | Rate Hike | Last Billed |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in recurring:
        hike = f"+${r['creep_diff']:.2f}" if r["price_creep"] else "None"
        print(f"| **{r['merchant']}** | {r['cadence']} | ${r['latest_cost']:.2f} \vert{} **${r['annual_drain']:,.2f}** | {hike} | {r['last_billed']} |")

    print("\n### Action Items")
    for r in recurring:
        if r["price_creep"]:
            print(f"- **Silent Creep Alert:** `{r['merchant']}` increased by `${r['creep_diff']:.2f}` since first transaction.")
        if r["annual_drain"] >= 500:
            print(f"- **High Drag:** `{r['merchant']}` consumes `${r['annual_drain']:,.2f}/yr`. Audit necessity.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python zombie_sub.py <statement_export.csv>")
        sys.exit(1)
    analyze_statement(sys.argv[1])
