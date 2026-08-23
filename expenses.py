import json 
import os
from datetime import datetime
EXPENSES_FILE = "expenses.json"
def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

def add_expense(amount, category="general"):
    expenses = load_expenses()
    expenses.append({
        "amount": amount,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    })
    save_expenses(expenses)

def get_total_expenses(period="all"):
    expenses = load_expenses()
    if not expenses:
        return "You haven't logged any expenses yet."

    today = datetime.now()
    filtered = []

    for e in expenses:
        expense_date = datetime.strptime(e["date"], "%Y-%m-%d")
        if period == "today" and expense_date.date() == today.date():
            filtered.append(e)
        elif period == "month" and expense_date.month == today.month and expense_date.year == today.year:
            filtered.append(e)
        elif period == "all":
            filtered.append(e)

    total = sum(e["amount"] for e in filtered)
    return f"You've spent {total} rupees {'today' if period == 'today' else 'this month' if period == 'month' else 'in total'}."



