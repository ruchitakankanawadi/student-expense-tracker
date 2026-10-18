import streamlit as st
import pandas as pd

from database import (
    create_table,
    add_expense,
    get_expenses,
    delete_expense
)

from chatbot import ask_chatbot
from summarizer import generate_expense_report, get_saving_tips
from image_generator import create_expense_chart


# Page configuration
st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Initialize database
create_table()


# Application title
st.title("💰 Student Expense Tracker")
st.write("Manage your money, track expenses, and save smarter!")


# Sidebar navigation
st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Add Expense",
        "Expense History",
        "Expense Analysis",
        "Expense Chatbot"
    ]
)


# Monthly budget
st.sidebar.header("💵 Monthly Budget")

budget = st.sidebar.number_input(
    "Enter Monthly Budget (₹)",
    min_value=0.0,
    value=5000.0,
    step=100.0
)


# Load expenses
expenses = get_expenses()

# Generate report
report = generate_expense_report(budget, expenses)


# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.header("📊 Expense Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Monthly Budget",
            f"₹{budget:.2f}"
        )

    with col2:
        st.metric(
            "Total Expenses",
            f"₹{report['total_spent']:.2f}"
        )

    with col3:
        st.metric(
            "Remaining Balance",
            f"₹{report['remaining_balance']:.2f}"
        )

    st.subheader("📈 Budget Usage")

    percentage = report["budget_used_percentage"]

    st.progress(
        min(max(percentage / 100, 0.0), 1.0)
    )

    st.write(f"Budget Used: {percentage:.2f}%")

    if report["budget_exceeded"]:
        st.error("⚠️ You have exceeded your budget!")

    elif percentage >= 80:
        st.warning("⚠️ You are close to your budget limit.")

    else:
        st.success("✅ Your spending is within your budget.")

    st.subheader("📊 Category-wise Spending")

    create_expense_chart(expenses)


# ---------------- ADD EXPENSE ----------------

elif menu == "Add Expense":

    st.header("💸 Add New Expense")

    with st.form("expense_form"):

        expense_name = st.text_input(
            "Expense Name"
        )

        amount = st.number_input(
            "Expense Amount (₹)",
            min_value=0.0,
            step=10.0
        )

        category = st.selectbox(
            "Select Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Hostel",
                "Entertainment",
                "Other"
            ]
        )

        expense_date = st.date_input(
            "Expense Date"
        )

        submit = st.form_submit_button(
            "Add Expense"
        )

        if submit:

            if expense_name.strip() and amount > 0:

                add_expense(
                    expense_name.strip(),
                    amount,
                    category,
                    expense_date.isoformat()
                )

                st.success("✅ Expense added successfully!")

            else:
                st.warning(
                    "Please enter a valid expense name and amount."
                )


# ---------------- EXPENSE HISTORY ----------------

elif menu == "Expense History":

    st.header("📋 Expense History")

    if expenses:

        df = pd.DataFrame(expenses)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗑️ Delete Expense")

        expense_options = {
            f"{e['id']} - {e['name']} - ₹{e['amount']}": e['id']
            for e in expenses
        }

        selected = st.selectbox(
            "Select Expense",
            list(expense_options.keys())
        )

        if st.button("Delete Selected Expense"):

            delete_expense(expense_options[selected])

            st.success("Expense deleted successfully!")

            st.rerun()

    else:
        st.info("No expenses found.")


# ---------------- EXPENSE ANALYSIS ----------------

elif menu == "Expense Analysis":

    st.header("📊 Expense Analysis")

    st.write(
        f"Total Spending: ₹{report['total_spent']:.2f}"
    )

    st.write(
        f"Remaining Balance: ₹{report['remaining_balance']:.2f}"
    )

    st.subheader("Category-wise Expenses")

    create_expense_chart(expenses)

    st.subheader("💡 Smart Saving Suggestions")

    tips = get_saving_tips(budget, expenses)

    for tip in tips:
        st.info(tip)


# ---------------- CHATBOT ----------------

elif menu == "Expense Chatbot":

    st.header("🤖 Student Expense Assistant")

    st.write(
        "Ask questions about budgeting, savings, and expenses."
    )

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Ask Chatbot"):

        if question.strip():

            response = ask_chatbot(
                question,
                budget,
                expenses
            )

            st.success(response)

        else:
            st.warning("Please enter a question.")


# Footer
st.divider()

st.caption(
    "Student Expense Tracker | Python + Streamlit + SQLite3"
)