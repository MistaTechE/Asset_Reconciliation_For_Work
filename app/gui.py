#gui.py
from tkinter import Tk, Button, messagebox, filedialog
from app.reconciler import reconcile
import pandas as pd
from pathlib import Path


def generate_report(root):
    messagebox.showinfo("Step 1", "Select CHECKOUTS CSV")
    checkouts_path = filedialog.askopenfilename(
        title="Select Checkouts CSV"
    )
    
    messagebox.showinfo("Step 2", "Select REPLACEMENTS CSV")
    replacements_path = filedialog.askopenfilename(
        title="Select Replacements CSV"
    )

    messagebox.showinfo("Step 3", "Select RETURNS CSV")
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

    desktop = Path.home() / "Desktop"

    result.to_csv(desktop / "students_to_call.csv", index=False)
    
    messagebox.showinfo("Success", "Call list generated successfully!")
    root.destroy()

def run_app():
    def center_window(root, width=500, height=300):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
    
    root = Tk()
    root.title("Asset Reconciliation Tool")
    center_window(root, 500, 300)
    root.configure(bg="#b2f5ea")

    button = Button(
        root,
        text="Generate Call List",
        command=lambda: generate_report(root),
        bg="#2dd4bf",      # teal button
        fg="black",
        padx=20,
        pady=10,
        relief="raised",
        borderwidth=3
    )
    
    button.pack(expand=True)

    button.bind("<Enter>", lambda e: button.config(bg="#14b8a6"))
    button.bind("<Leave>", lambda e: button.config(bg="#2dd4bf"))

    root.mainloop()
