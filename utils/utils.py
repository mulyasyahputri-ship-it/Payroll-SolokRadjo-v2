import pandas as pd

import streamlit as st

def rupiah(x):
    if pd.isna(x):
        return "Rp0"

    if isinstance(x, str):
        x = x.replace(".", "").replace(",", ".")
        try:
            x = float(x)
        except:
            return "Rp0"

    if isinstance(x, (int, float)):
        if abs(x) < 10000:
            x *= 1000

        return f"Rp{int(round(x)):,}".replace(",", ".")

    return "Rp0"

def get_number_column_config(columns):
    config = {}

    for col in columns:
        config[col] = st.column_config.NumberColumn(
            label=col,
            format="%d",
            step=1
        )
    return config


def to_int(value):
    if value is None or value == "":
        return 0

    if isinstance(value, (int, float)):
        return int(value)

    value = str(value)

    value = value.replace("Rp", "")
    value = value.replace(".", "")
    value = value.replace(",", "")
    value = value.strip()

    return int(value)

def clean_number(value):
    if pd.isna(value):
        return 0
    
    if isinstance(value, (int,
                          float)):
        return int(value)
    value = (
        str(value)
        .replace("Rp", "")
        .replace(".", "")
        .replace(",", "")
        .replace(" ", "")
    )

    try:
        return int(float(value))
    except:
        return 0

def format_rupiah(value):
    value = clean_number(value)
    return f"{value:,.0f}".replace(",", ".")