def group_by_month(transactions):
    txn_per_month = {}
    for txn in transactions:
        date = txn.get("date", "")
        if date:
            month = date[:7]  # Extract "YYYY-MM" from "YYYY-MM-DD"
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