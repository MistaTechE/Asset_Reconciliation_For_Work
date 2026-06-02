#gui.py
from tkinter import Tk, Button
from app.csv_loader import load_checkouts, load_replacements, load_returns
from app.reconciler import reconcile


def generate_report():
    checkouts = load_checkouts()
    replacements = load_replacements()
    returns = load_returns()

    result = reconcile(checkouts, replacements, returns)

    result.to_csv("data/output/students_to_call.csv", index=False)


def run_app():
    root = Tk()

    Button(
        root,
        text="Generate Call List",
        command=generate_report
    ).pack()

    root.mainloop()
