#csv_loader.py
import pandas as pd

def load_checkouts():
    return pd.read_csv("data/input/checkouts.csv", dtype=str)

def load_replacements():
    return pd.read_csv("data/input/replacements.csv", dtype=str)

def load_returns():
    return pd.read_csv("data/input/returns.csv", dtype=str)
