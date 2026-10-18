def ask_chatbot(question, budget, expenses):

    question = question.lower().strip()

    total_spent = sum(
        float(expense["amount"])
        for expense in expenses
    )

    remaining = budget - total_spent

    if "hello" in question or question == "hi":

        return (
            "Hello! 👋 I am your Student Expense Assistant. "
            "How can I help you?"
        )

    elif "total" in question or "spent" in question:

        return f"You have spent ₹{total_spent:.2f} so far."

    elif "remaining" in question or "balance" in question:

        return f"Your remaining balance is ₹{remaining:.2f}."

    elif "budget" in question:

        return f"Your current budget is ₹{budget:.2f}."

    elif "save" in question or "saving" in question:

        return (
            "Try saving a small amount every day. "
            "Avoid unnecessary shopping and track your expenses."
        )

    elif "food" in question:

        food_total = sum(
            float(expense["amount"])
            for expense in expenses
            if expense["category"].lower() == "food"
        )

        return f"You have spent ₹{food_total:.2f} on food."

    elif "expense" in question:

        return (
            f"You have recorded {len(expenses)} expenses "
            f"with total spending of ₹{total_spent:.2f}."
        )

    else:

        return (
            "I can help you with your budget, expenses, "
            "remaining balance, food spending, and saving tips."
        )