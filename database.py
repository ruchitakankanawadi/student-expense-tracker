import sqlite3
from datetime import date
from pathlib import Path


# Use a new database to avoid conflicts
# with the previous database structure
DB_NAME = Path(__file__).resolve().parent / "student_tracker_v2.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# Create table
def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add expense
def add_expense(name, amount, category, expense_date=None):

    if expense_date is None:
        expense_date = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (name, amount, category, expense_date)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        float(amount),
        category,
        expense_date
    ))

    conn.commit()
    conn.close()


# Get expenses
def get_expenses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, amount, category, expense_date
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    expenses = []

    for row in rows:

        expenses.append({
            "id": row[0],
            "name": row[1],
            "amount": float(row[2]),
            "category": row[3],
            "expense_date": row[4]
        })

    return expenses


# Delete expense
def delete_expense(expense_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Database created successfully!")