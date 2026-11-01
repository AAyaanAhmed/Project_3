import json
import os
from datetime import datetime

FILE = "expenses.json"


def load_data():
    if not os.path.exists(FILE):
        return {"expenses": [], "budgets": {}}
    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_expense(data):
    try:
        amount = float(input("Amount: ₹"))
    except ValueError:
        print("Invalid amount.")
        return

    expense = {
        "date": input("Date (YYYY-MM-DD, Enter=today): ")
        or datetime.now().strftime("%Y-%m-%d"),
        "category": input("Category: "),
        "note": input("Description: "),
        "amount": amount
    }

    data["expenses"].append(expense)
    save_data(data)
    print("Expense added.")


def view_expenses(data):
    if not data["expenses"]:
        print("No expenses found.")
        return

    print("\nExpenses")
    print("-" * 50)
    for i, e in enumerate(data["expenses"], 1):
        print(f"{i}. {e['date']} | {e['category']} | {e['note']} | ₹{e['amount']}")


def delete_expense(data):
    view_expenses(data)

    try:
        index = int(input("Delete expense number: ")) - 1
        data["expenses"].pop(index)
        save_data(data)
        print("Expense deleted.")
    except:
        print("Invalid selection.")


def set_budget(data):
    month = input("Month (YYYY-MM): ")

    try:
        data["budgets"][month] = float(input("Budget: ₹"))
        save_data(data)
        print("Budget saved.")
    except ValueError:
        print("Invalid amount.")


def summary(data):
    total = 0
    category_total = {}

    for e in data["expenses"]:
        total += e["amount"]
        category_total[e["category"]] = category_total.get(e["category"], 0) + e["amount"]

    print("\nCategory Summary")
    print("-" * 25)
    for c, a in category_total.items():
        print(f"{c}: ₹{a}")

    print(f"\nTotal Spent: ₹{total}")


def search(data):
    key = input("Search: ").lower()

    found = False
    for e in data["expenses"]:
        if key in e["category"].lower() or key in e["note"].lower():
            print(e)
            found = True

    if not found:
        print("No matching records.")


def monthly_report(data):
    month = input("Month (YYYY-MM): ")

    spent = sum(
        e["amount"] for e in data["expenses"]
        if e["date"].startswith(month)
    )

    budget = data["budgets"].get(month)

    print(f"\nSpent: ₹{spent}")

    if budget is not None:
        print(f"Budget: ₹{budget}")
        print(f"Remaining: ₹{budget - spent}")
    else:
        print("Budget not set.")


def main():
    data = load_data()

    while True:
        print("""
====== Expense Tracker ======
1. Add Expense
2. View Expenses
3. Delete Expense
4. Set Budget
5. Spending Summary
6. Search Expense
7. Monthly Report
8. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            add_expense(data)
        elif choice == "2":
            view_expenses(data)
        elif choice == "3":
            delete_expense(data)
        elif choice == "4":
            set_budget(data)
        elif choice == "5":
            summary(data)
        elif choice == "6":
            search(data)
        elif choice == "7":
            monthly_report(data)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
