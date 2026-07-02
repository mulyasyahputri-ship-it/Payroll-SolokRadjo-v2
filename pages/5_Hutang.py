import streamlit as st
import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

from database.google_sheet_solokradjo_one import (
    get_sheet_df,
    hutang_ws
)

df = get_sheet_df("HUTANG")


kolom_nominal = [
    "SALDO PINJAMAN",
    "CICILAN",
    "SISA PINJAMAN"
]

from utils.utils import get_number_column_config

edited_df = st.data_editor(
    df,
    column_config=get_number_column_config(kolom_nominal),
    use_container_width=True,
    num_rows="dynamic"
)

for kolom in kolom_nominal:

    if kolom in df.columns:

        df[kolom] = (
            df[kolom]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        df[kolom] = (
            pd.to_numeric(
                df[kolom],
                errors="coerce"
            )
            .fillna(0)
        )

        df[kolom] = (
            df[kolom]
            .apply(
                lambda x: x * 1000 if 0 < x < 10000 else x
            )
            .astype(int)
        )

# ==========================================
# TITLE
# ==========================================

st.title("💳 Data Hutang")

st.write("Input data hutang karyawan setiap periode.")

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
    use_container_width=True,
    num_rows="dynamic"
)

# ==========================================
# SAVE
# ==========================================

if st.button(
    "💾 Save Hutang",
    use_container_width=True
):

    hutang_ws.update(
        "A1"
    [edited_df.columns.values.tolist()]
    + edited_df.values.tolist()
    )
st.success("Data hutang berhasil disimpan!")
st.rerun()