import streamlit as st
import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

from database.google_sheet_solokradjo_one import (
    get_sheet_df,
    benefit_ws
)

from utils.utils import get_number_column_config

df = get_sheet_df("BENEFIT")

kolom_angka = [
    "GAJI POKOK",
    "BONUS",
    "TUNJANGAN JABATAN",
    "TUNJANGAN KINERJA",
    "TUNJANGAN PENDIDIKAN ANAK",
    "BPJS KESEHATAN KARYAWAN",
    "BPJS TK KARYAWAN",
    "BPJS KESEHATAN PERUSAHAAN",
    "BPJS TK PERUSAHAAN",
    "TUNJANGAN MAKAN MINUM",
    "TEMPAT TINGGAL"
]

for kolom in kolom_angka:
    if kolom in df.columns:
        df[kolom] = (
            pd.to_numeric(
                df[kolom]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", "", regex=False),
                errors="coerce"
            )
            .fillna(0)
            .astype("Int64")
        )


# ==========================================
# TITLE
# ==========================================

st.title("🎁 Data Benefit")

st.write("Input benefit karyawan setiap periode.")


unit_list = ["Semua"] + sorted(df["NAMA UNIT"].dropna().unique().tolist())
selected_unit = st.selectbox(
    "Pilih Cabang",
    unit_list
    )

if selected_unit != "Semua":
    df = df[df["NAMA UNIT"] ==
            selected_unit]

# ==========================================
# DATA EDITOR
# ==========================================


edited_df = st.data_editor(
    df,
    column_config=get_number_column_config(kolom_angka),
    use_container_width=True,
    num_rows="dynamic"
)



# ==========================================
# SAVE
# ==========================================

if st.button(
    "💾 Save Benefit",
    use_container_width=True
):
    
    benefit_ws.update(
        "A1",
    [edited_df.columns.values.tolist()]
    + edited_df.values.tolist()
    )
st.success("Benefit berhasil disimpan!")

