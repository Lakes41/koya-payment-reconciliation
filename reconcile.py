#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""

import json
from datetime import datetime
from decimal import Decimal

payments = {}

with open("payments.jsonl") as file:
    for line in file:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(event, dict) or not event.get("txn_id"):
            continue

        txn_id = event["txn_id"]
        time = datetime.fromisoformat(event["ts"].replace("Z", "+00:00"))

        if txn_id not in payments or time >= payments[txn_id][0]:
            payments[txn_id] = (time, event)

count = 0
total = Decimal("0")

for time, event in payments.values():
    if event["status"] == "success":
        count += 1
        amount = str(event["amount"]).replace(",", "").replace("₦", "").strip()
        total += Decimal(amount)

with open("expected.txt") as file:
    expected = int(file.read().strip())

if count == expected:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
else:
    print(f"Check failed: counted {count}, expected {expected}.")
