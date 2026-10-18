import streamlit as st
import pandas as pd


def create_expense_chart(expenses):

    if not expenses:

        st.info(
            "No expenses available to display charts."
        )

        return

    df = pd.DataFrame(expenses)

    category_totals = (
        df.groupby("category")["amount"]
        .sum()
    )

    st.bar_chart(category_totals)

    st.subheader("📊 Spending Distribution")

    st.dataframe(
        category_totals.reset_index(
            name="Total Amount"
        ),
        use_container_width=True,
        hide_index=True
    )