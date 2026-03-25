import csv
import os
import json
import anthropic
from dotenv import load_dotenv

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

def categorize_with_claude(client, transaction):    
    response = client.messages.create(
        messages=[{"role": "user", "content": json.dumps(transaction)}],
        max_tokens=1024,
        model="claude-sonnet-4-20250514",
        system= """You are a transaction categorizer. Respond ONLY with valid JSON. No extra text, no markdown.
        Categorize the transaction into one of these categories: Food, Transport, Entertainment, Utilities, Shopping.
        If none fit, use "Other".
        Use exactly this structure:
        {"category": "Food"}"""
    )

    category = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    try:
        return json.loads(category), input_tokens, output_tokens
    except json.JSONDecodeError:
        pass

    start = category.find("{")
    end = category.rfind("}") + 1

    if start != -1 and end > start:
        try:
            claude_category = json.loads(category[start:end])
            return claude_category, input_tokens, output_tokens
        except json.JSONDecodeError:
            pass
    
    return None, input_tokens, output_tokens

def batch_categorize(client, transactions):
    results = []
    input_tokens = 0
    output_tokens = 0

    for i, transaction in enumerate(transactions):
        if transaction["category"]:
            continue
        
        attempts = 0
        while attempts < 3:
            try:
                category, call_input_tokens, output = categorize_with_claude(client, transaction)
                input_tokens += call_input_tokens
                output_tokens += output
                if category:
                    results.append(f"Description: {transaction['description']}, Category: {category['category']}")
                    break
                else:
                    attempts += 1
            except Exception as e:
                print(f"Error categorizing transaction: {e}")
                attempts += 1

    return results, input_tokens, output_tokens


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

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

create_mock_csv("transactions.csv", transactions)
transactions = read_transaction("transactions.csv")
results, input_tokens, output_tokens = batch_categorize(client, transactions)

print("Categorization Results:")
for result in results:
    print(result)
print(f"Total Input Tokens: {input_tokens}")
print(f"Total Output Tokens: {output_tokens}")