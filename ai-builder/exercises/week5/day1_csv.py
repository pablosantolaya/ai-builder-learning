import csv

def create_mock_csv(filepath, transactions):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["date", "description", "amount", "category"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

def read_transaction(filepath):
    reader_float = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            reader_float.append(row)
    return reader_float

def filter_and_save(transactions, min_amount, output_path):
    top_transactions = [row for row in transactions if row["amount"] > min_amount]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = transactions[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(top_transactions)

def validate_transactions(transactions):
    valid = []
    errors = []

    for i, row in enumerate(transactions):
        if not row.get("description"):
            errors.append(f"Row {i + 1}: missing description")
            continue

        if not row.get("date"):
            errors.append(f"Row {i + 1}: missing date")
            continue

        try:
            amount = float(row["amount"])
            if amount <= 0:
                errors.append(f"Row {i + 1}: amount must be positive")
                continue
        except (ValueError, KeyError):
            errors.append(f"Row {i + 1}: invalid amount")
            continue

        valid.append(row)
    
    return valid, errors

def total_spending(transactions):
    sum_amount = 0
    for transaction in transactions:
        sum_amount += transaction["amount"]
    return sum_amount

def spending_by_category(transactions):
    sum_category = {}
    for transaction in transactions:
        sum_category[transaction["category"]] = sum_category.get(transaction["category"], 0) + transaction["amount"]
    return sum_category

def top_n_transactions(transactions, n=5):
    top_transactions = sorted(transactions, key=lambda transaction: transaction["amount"], reverse=True)
    return top_transactions[0:n]

def categorize_by_keyword(transactions):
    keywords = {
        "Transport": ["uber", "lyft"],
        "Food": ["starbucks", "restaurant", "lunch", "grocery"],
        "Entertainment": ["netflix", "headphones"],
    }
    
    categorized = 0
    for transaction in transactions:
        if transaction["category"]:
            continue
        
        desc = transaction["description"].lower()
        for category, words in keywords.items():
            if any(word in desc for word in words):
                transaction["category"] = category
                categorized += 1
                break
    
    return categorized


transactions = [
    {"date": "2026-03-01", "description": "", "amount": "5.50", "category": "Food"},
    {"date": "2026-03-02", "description": "Uber to airport", "amount": "-42.00", "category": "Transport"},
    {"date": "2026-03-03", "description": "Electric bill", "amount": "87.30", "category": "Utilities"},
    {"date": "2026-03-05", "description": "Amazon purchase", "amount": "129.99", "category": "Shopping"},
    {"date": "2026-03-07", "description": "Grocery store", "amount": "63.20", "category": "Food"},
    {"date": "2026-03-10", "description": "Netflix", "amount": "15.99", "category": "Entertainment"},
    {"date": "2026-03-12", "description": "Corner deli lunch", "amount": "11.75", "category": ""},
    {"date": "2026-03-15", "description": "Lyft downtown", "amount": "18.50", "category": ""},
    {"date": "2026-03-18", "description": "New headphones", "amount": "79.99", "category": ""},
    {"date": "2026-03-20", "description": "Water bill", "amount": "45.00", "category": "Utilities"},
]

create_mock_csv("exercises/week5/output/transactions.csv", transactions)
transactions_float = read_transaction("exercises/week5/output/transactions.csv")
print(transactions_float[:5])
filter_and_save(transactions_float, min_amount=50.0, output_path="exercises/week5/output/top_transactions.csv")

valid, errors = validate_transactions(transactions_float)
print(f"\nValid: {len(valid)}, Errors: {len(errors)}")
for e in errors:
    print(e)

print(f"\nTotal spending: ${total_spending(valid):.2f}")
print(f"\nSpending by category: {spending_by_category(valid)}")
print(f"\nTop 3 transactions: {top_n_transactions(valid, 3)}")

count = categorize_by_keyword(valid)
print(f"\nCategorized {count} transactions by keyword")
print(f"Updated categories: {spending_by_category(valid)}")