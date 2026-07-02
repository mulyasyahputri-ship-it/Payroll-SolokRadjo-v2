import pandas as pd

from database.google_sheet_solokradjo_one import spreadsheet

from utils.utils import clean_number

from modules.absensi_engine import update_absensi
from modules.benefit_engine import update_benefit
from modules.hutang_engine import update_hutang
from modules.payroll_engine import calculate_payroll


# ==========================================
# LOAD MASTER KARYAWAN
# ==========================================

def load_karyawan(unit):

    worksheet = spreadsheet.worksheet("KARYAWAN")

    print(worksheet.title)
    print(worksheet.row_values(1))

    data = worksheet.get_all_records()

    df = pd.DataFrame(data)

    kolom_angka = [
        "GAJI POKOK",
        "BONUS",
        "TUNJANGAN JABATAN",
        "TUNJANGAN KINERJA",
        "UPAH LEMBUR",
        "BPJS KES KARYAWAN",
        "BPJS TK KARYAWAN",
        "BPJS KES PERUSAHAAN",
        "BPJS TK PERUSAHAAN",
        "TUNJANGAN MAKAN MINUM",
        "TEMPAT TINGGAL"
    ]

    for kolom in kolom_angka:
        if kolom in df.columns:
            df[kolom] = df[kolom].apply(clean_number)
    

    # Hanya karyawan aktif
    if "STATUS" in df.columns:
        df = df[
            df["STATUS"].str.upper() == "AKTIF"
        ]

    # Filter unit
    if unit != "Semua":
        df = df[
            df["NAMA UNIT"] == unit
        ]

    return df.reset_index(drop=True)


# ==========================================
# MERGE PAYROLL
# ==========================================

def merge_payroll(periode, unit):

    df = load_karyawan(unit)

    df = update_absensi(
        df,
        periode
    )

    df = update_benefit(
        df,
        periode
    )

    df = update_hutang(
        df,
        periode
    )

    df = calculate_payroll(
        df,
        periode
    )

    return df