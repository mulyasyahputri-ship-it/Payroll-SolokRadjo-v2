import streamlit as st
import pandas as pd

from database.google_sheet_solokradjo_one import spreadsheet
from utils.utils import rupiah

st.set_page_config(
    page_title="Laporan Payroll",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Laporan Payroll")
st.caption("Riwayat Payroll Karyawan Solok Radjo")

# ==========================
# LOAD DATA
# ==========================

worksheet = spreadsheet.worksheet("PAYROLL")

data = worksheet.get_all_records()

df = pd.DataFrame(data)

# ==========================
# FILTER
# ==========================

col1, col2, col3 = st.columns(3)

with col1:
    periode = st.selectbox(
        "Periode",
        sorted(df["PERIODE"].unique(), reverse=True)
    )

with col2:
    unit = st.selectbox(
        "NAMA UNIT",
        ["Semua"] + sorted(df["NAMA UNIT"].unique())
    )

with col3:
    keyword = st.text_input("Cari Nama Karyawan")

# ==========================
# FILTER DATA
# ==========================

df_show = df[df["PERIODE"] == periode]

if unit != "Semua":
    df_show = df_show[df_show["NAMA UNIT"] == unit]

if keyword:
    df_show = df_show[
        df_show["NAMA KARYAWAN"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

# ==========================
# SUMMARY
# ==========================

jumlah_karyawan = len(df_show)

total_payroll = pd.to_numeric(
    df_show["GAJI DITERIMA"],
    errors="coerce"
).fillna(0).sum()

total_benefit = pd.to_numeric(
    df_show["JUMLAH BENEFIT"],
    errors="coerce"
).fillna(0).sum()

total_lembur = pd.to_numeric(
    df_show["UPAH LEMBUR"],
    errors="coerce"
).fillna(0).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Jumlah Karyawan",
    jumlah_karyawan
)

col2.metric(
    "Total Payroll",
    rupiah(total_payroll)
)

col3.metric(
    "Total Benefit",
    rupiah(total_benefit)
)

col4.metric(
    "Total Lembur",
    rupiah(total_lembur)
)

st.divider()

# ==========================
# FORMAT
# ==========================

kolom_uang = [
    "GAJI DITERIMA",
    "JUMLAH BENEFIT",
    "TOTAL GAJI & BENEFIT",
    "UPAH LEMBUR"
]

df_tampil = df_show.copy()

for kolom in kolom_uang:
    if kolom in df_tampil.columns:
        df_tampil[kolom] = df_tampil[kolom].apply(rupiah)

# ==========================
# TABEL
# ==========================

st.dataframe(
    df_tampil,
    use_container_width=True,
    hide_index=True
)