import pandas as pd
from datetime import datetime

from database.google_sheet_solokradjo_one import spreadsheet


def approve_payroll(df, periode):

    ws = spreadsheet.worksheet("PAYROLL")

    data = df.copy()

    # tambah periode
    data["PERIODE"] = periode

    # tambah tanggal approve
    data["TANGGAL APPROVE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # sementara payroll id sederhana
    data["PAYROLL ID"] = [
        f"PR-{periode}-{i+1:04d}"
        for i in range(len(data))
    ]

    # urutan kolom
    kolom_awal = [
        "PERIODE",
        "PAYROLL ID",
        "TANGGAL APPROVE"
    ]

    kolom_lain = [
        c for c in data.columns
        if c not in kolom_awal
    ]

    data = data[kolom_awal + kolom_lain]

    ws.append_rows(
        data.values.tolist(),
        value_input_option="USER_ENTERED"
    )

    return True

