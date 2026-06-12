#gui.py
from tkinter import Tk, Button, messagebox, filedialog
from app.csv_loader import load_checkouts, load_replacements, load_returns
from app.reconciler import reconcile
import pandas as pd


def generate_report():
    checkouts_path = filedialog.askopenfilename(
        title="Select Checkouts CSV"
    )

    replacements_path = filedialog.askopenfilename(
        title="Select Replacements CSV"
    )

    returns_path = filedialog.askopenfilename(
        title="Select Returns CSV"
    )

    if not checkouts_path or not replacements_path or not returns_path:
        messagebox.showwarning("Cancelled", "File selection cancelled, must have three files.")
        return

    checkouts = pd.read_csv(checkouts_path, dtype=str)
    replacements = pd.read_csv(replacements_path, dtype=str)
    returns = pd.read_csv(returns_path, dtype=str)

    result = reconcile(checkouts, replacements, returns)

    result.to_csv("data/output/students_to_call.csv", index=False)
    
    messagebox.showinfo("Success", "Call list generated successfully!")


def run_app():
    root = Tk()

    Button(
        root,
        text="Generate Call List",
        command=generate_report
    ).pack(padx=20, pady=20)

    root.mainloop()
