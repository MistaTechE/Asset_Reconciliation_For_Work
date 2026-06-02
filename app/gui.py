#gui.py

from app.csv_loader import load_checkouts, load_replacements, load_returns
from app.reconciler import reconcile


def generate_report():
    checkouts = load_checkouts()
    replacements = load_replacements()
    returns = load_returns()

    result = reconcile(checkouts, replacements, returns)

    result.to_csv("data/output/students_to_call.csv", index=False)
