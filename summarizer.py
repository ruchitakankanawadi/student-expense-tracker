def generate_expense_report(budget, expenses):

    total_spent = sum(
        float(expense["amount"])
        for expense in expenses
    )

    remaining_balance = budget - total_spent

    if budget > 0:
        budget_used_percentage = (
            total_spent / budget
        ) * 100
    else:
        budget_used_percentage = 0

    category_totals = {}

    for expense in expenses:

        category = expense["category"]
        amount = float(expense["amount"])

        category_totals[category] = (
            category_totals.get(category, 0)
            + amount
        )

    return {
        "total_spent": total_spent,
        "remaining_balance": remaining_balance,
        "budget_used_percentage": budget_used_percentage,
        "budget_exceeded": total_spent > budget,
        "category_totals": category_totals
    }


def get_saving_tips(budget, expenses):

    tips = []

    report = generate_expense_report(
        budget,
        expenses
    )

    total_spent = report["total_spent"]

    if budget <= 0:

        tips.append(
            "💰 Set a monthly budget to manage your spending."
        )

    elif total_spent > budget:

        tips.append(
            "⚠️ You have exceeded your budget. "
            "Reduce unnecessary expenses."
        )

    elif total_spent > budget * 0.8:

        tips.append(
            "⚠️ You have used more than 80% of your budget."
        )

    else:

        tips.append(
            "✅ Good job! Your spending is within your budget."
        )

    category_totals = report["category_totals"]

    if category_totals:

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        tips.append(
            f"📊 Your highest spending category is "
            f"{highest_category}."
        )

    tips.append(
        "💡 Try saving at least ₹10 every day."
    )

    tips.append(
        "📝 Record your expenses daily."
    )

    return tips