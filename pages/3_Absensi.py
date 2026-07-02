import streamlit as st
from database.google_sheet_solokradjo_one import spreadsheet
import pandas as pd
import streamlit as st

worksheet = spreadsheet.worksheet("ABSENSI")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.title("🗓️ Data Absensi")

st.write("Input benefit karyawan setiap periode.")

unit_list = ["Semua"] + sorted(df["NAMA UNIT"].dropna().unique().tolist())
selected_unit = st.selectbox(
    "Pilih Cabang",
    unit_list
    )

if selected_unit != "Semua":
    df = df[df["NAMA UNIT"] ==
            selected_unit]

st.dataframe(df, use_container_width=True)