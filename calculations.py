def generate_expense_report(budget, expenses, days_tracked=1):

    total_spent = sum(
        float(expense["amount"]) for expense in expenses
    )

    remaining_balance = budget - total_spent

    budget_used_percentage = (
        (total_spent / budget) * 100 if budget > 0 else 0
    )

    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = float(expense["amount"])

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    return {
        "total_spent": total_spent,
        "remaining_balance": remaining_balance,
        "budget_used_percentage": budget_used_percentage,
        "budget_exceeded": total_spent > budget,
        "category_totals": category_totals
    }