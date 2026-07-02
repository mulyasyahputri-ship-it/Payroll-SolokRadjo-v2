import streamlit as st
import pandas as pd

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from database.google_sheet_solokradjo_one import get_sheet_df

df = get_sheet_df("KARYAWAN")

st.title("👥 Data Karyawan")

st.write("Data karyawan Solok Radjo")
st.write("Input benefit karyawan setiap periode.")

unit_list = ["Semua"] + sorted(df["NAMA UNIT"].dropna().unique().tolist())

selected_unit = st.selectbox(
    "Pilih Cabang",
    unit_list
)

if selected_unit != "Semua":
    df = df[df["NAMA UNIT"] == selected_unit]

st.dataframe(
    df,
    use_container_width=True
)