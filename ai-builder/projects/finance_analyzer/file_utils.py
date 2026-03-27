"""
file_utils.py — File reading and writing utilities for the Finance Analyzer.

Handles:
  - Reading and validating the CSV bank export
  - Saving the final report as JSON and plain text
"""

import csv
import json
import os


# ── Reading ────────────────────────────────────────────────────────────────────

def read_and_validate_csv(filepath):
    """
    Read a bank CSV file and validate every row.

    DictReader turns each row into a dict using the header row as keys.
    For example: {"Posted Date": "2024-01-15", "Payee": "Starbucks", ...}

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        tuple: (valid_transactions, errors)
            - valid_transactions: list of dicts with keys: date, payee, amount (float)
            - errors: list of strings describing any rows that were skipped
    """
    valid_transactions = []
    errors = []

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)   # reads the first row as column names automatically

        for row_number, row in enumerate(reader, start=2):  # start=2 because row 1 is the header

            # ── Validate: Posted Date must be present ──────────────────────────
            date = row.get("Posted Date", "").strip()
            if not date:
                errors.append(f"Row {row_number}: missing 'Posted Date' — skipped")
                continue

            # ── Validate: Amount must convert to a float ───────────────────────
            raw_amount = row.get("Amount", "").strip()
            try:
                amount = float(raw_amount)
            except ValueError:
                errors.append(f"Row {row_number}: invalid Amount '{raw_amount}' — skipped")
                continue

            # ── Skip credits and payments (positive amounts) ───────────────────
            # Real bank exports show expenses as negative numbers.
            # Positive amounts are credits (e.g. payments made to the account) —
            # we skip these since we only want to analyze spending.
            if amount >= 0:
                continue

            # Convert negative expense to a positive spending amount
            amount = abs(amount)

            # ── Build the clean transaction dict ───────────────────────────────
            # We only keep the three fields we care about.
            # Reference Number and Address columns are intentionally ignored.
            payee = row.get("Payee", "").strip()

            valid_transactions.append({
                "date":   date,
                "payee":  payee,
                "amount": amount,   # positive float, e.g. 42.45
            })

    return valid_transactions, errors


# ── Writing ────────────────────────────────────────────────────────────────────

def save_json_report(report, output_dir, timestamp):
    """
    Save the report dict as a JSON file.

    os.makedirs with exist_ok=True creates the folder (and any parents)
    if it doesn't already exist — safe to call even if it already exists.

    Args:
        report (dict): The full analysis report.
        output_dir (str): Folder to write into.
        timestamp (str): String like "20240115_143022" to make the filename unique.
    """
    os.makedirs(output_dir, exist_ok=True)

    filename = f"report_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        # indent=2 makes the JSON human-readable with nice indentation
        json.dump(report, f, indent=2)

    print(f"  JSON report saved -> {filepath}")
    return filepath


def save_text_report(report, output_dir, timestamp):
    """
    Save the report as a plain-text summary (easy to read without tools).

    Args:
        report (dict): The full analysis report.
        output_dir (str): Folder to write into.
        timestamp (str): String like "20240115_143022" to make the filename unique.
    """
    os.makedirs(output_dir, exist_ok=True)

    filename = f"report_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    # Pull the summary section out of the report dict
    s = report.get("summary", {})
    monthly_trends = report.get("monthly_trends", {})

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("   PERSONAL FINANCE REPORT\n")
        f.write(f"   Generated: {timestamp}\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Total Spending:      ${s.get('total_spending', 0):.2f}\n")
        f.write(f"Transactions:        {s.get('transaction_count', 0)}\n")
        f.write(f"Daily Average:       ${s.get('daily_average', 0):.2f}\n")
        f.write(f"Categories Used:     {s.get('category_count', 0)}\n\n")

        f.write("── Spending by Category ──────────────────────\n")
        # Sort categories by amount (highest first) for easy scanning
        by_cat = s.get("spending_by_category", {})
        for category, total in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
            f.write(f"  {category:<15} ${total:.2f}\n")

        f.write("\n── Top Transactions ──────────────────────────\n")
        for txn in s.get("top_n_transactions", []):
            f.write(f"  {txn['date']}  {txn['payee']:<25} ${txn['amount']:.2f}  [{txn.get('category', '?')}]\n")

        f.write("\n── Monthly Trends ────────────────────────── \n")
        # Sort months chronologically for easy scanning
        for month, data in sorted(monthly_trends.items()):
            f.write(f"  {month}: ${data['total']:.2f} total\n")
            for category, amount in sorted(data["category_totals"].items(), key=lambda x: x[1], reverse=True):
                f.write(f"    {category:<15} ${amount:.2f}\n")

    print(f"  Text report saved  -> {filepath}")
    return filepath
