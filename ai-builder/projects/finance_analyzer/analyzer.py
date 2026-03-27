"""
analyzer.py — Pure calculation logic for the Finance Analyzer.

No API calls here — just math on the categorized transactions.
Takes a list of transactions and returns a summary dict.
"""
def group_by_month(transactions):
    txn_per_month = {}
    for txn in transactions:
        date = txn.get("date", "")
        if date:
            month = f"{date[6:]}-{date[:2]}"  # Extract "YYYY-MM" from "YYYY-MM-DD"
            if month not in txn_per_month:
                txn_per_month[month] = []
            txn_per_month[month].append(txn)
    return txn_per_month


def calculate_monthly_trends(transactions):
    monthly_trends = {}
    for month, txns in sorted(group_by_month(transactions).items()):
        category_totals = {}
        for txn in txns:
            category = txn.get("category", "Other")
            amount = txn["amount"]
            category_totals[category] = category_totals.get(category, 0) + amount
        total = sum(txn["amount"] for txn in txns)
        monthly_trends[month] = {"total": round(total, 2), "category_totals": {k: round(v, 2) for k, v in category_totals.items()}}
    return monthly_trends


def calculate_summary(transactions, top_n):
    """
    Calculate spending statistics from a list of categorized transactions.

    Uses .get(key, 0) for accumulation — this is a common pattern:
    if the key doesn't exist yet, default to 0, then add to it.

    Args:
        transactions (list): Categorized transactions — each is a dict with
                             keys: date, payee, amount (float), category (str).
        top_n (int): How many top transactions to include in the summary.

    Returns:
        dict with keys:
            total_spending       (float)  — sum of all amounts
            spending_by_category (dict)   — {category: total_amount}
            top_n_transactions   (list)   — top N transactions sorted by amount desc
            daily_average        (float)  — total / number of unique days
            transaction_count    (int)    — total number of transactions
            category_count       (int)    — number of distinct categories used
    """

    # ── Totals ─────────────────────────────────────────────────────────────────
    total_spending = 0.0
    spending_by_category = {}   # will look like {"Food": 45.20, "Transport": 32.10, ...}
    unique_dates = set()        # a set automatically ignores duplicates

    for txn in transactions:
        amount = txn["amount"]
        category = txn.get("category", "Other")
        date = txn.get("date", "")

        # Add to the grand total
        total_spending += amount

        # Accumulate per-category total.
        # .get(category, 0) returns 0 if this category hasn't appeared yet.
        spending_by_category[category] = spending_by_category.get(category, 0) + amount

        # Track unique dates so we can compute a daily average
        if date:
            unique_dates.add(date)

    # ── Derived stats ──────────────────────────────────────────────────────────
    transaction_count = len(transactions)
    category_count = len(spending_by_category)

    # Avoid dividing by zero if all rows had missing dates
    num_days = len(unique_dates) if unique_dates else 1
    daily_average = total_spending / num_days

    # ── Top N transactions ─────────────────────────────────────────────────────
    # sorted() returns a NEW list — it doesn't change the original.
    # key=lambda txn: txn["amount"] tells sorted() what value to sort by.
    # reverse=True means highest amount first.
    sorted_transactions = sorted(transactions, key=lambda txn: txn["amount"], reverse=True)
    top_n_transactions = sorted_transactions[:top_n]   # slice to keep only the top N

    # ── Round floats for clean output ─────────────────────────────────────────
    # Floating-point math can produce values like 45.199999999 — round to 2 decimals.
    total_spending = round(total_spending, 2)
    daily_average = round(daily_average, 2)
    spending_by_category = {k: round(v, 2) for k, v in spending_by_category.items()}

    return {
        "total_spending":       total_spending,
        "spending_by_category": spending_by_category,
        "top_n_transactions":   top_n_transactions,
        "daily_average":        daily_average,
        "transaction_count":    transaction_count,
        "category_count":       category_count,
    }
