import gspread
import streamlit as st
import pandas as pd

gc = gspread.service_account(

filename="msp-payroll-system-6caa7172d0c4.json"
)

spreadsheet = gc.open("MSP_PAYROLL_DATABASE")

# Worksheet
karyawan_ws = spreadsheet.worksheet("KARYAWAN")
absensi_ws = spreadsheet.worksheet("ABSENSI")
benefit_ws = spreadsheet.worksheet("BENEFIT")
hutang_ws = spreadsheet.worksheet("HUTANG")
payroll_input_ws = spreadsheet.worksheet("PAYROLL_INPUT")
payroll_ws = spreadsheet.worksheet("PAYROLL")

@st.cache_data(ttl=60)
def load_sheet(sheet_name):
    worksheet = spreadsheet.worksheet(sheet_name)
    return worksheet.get_all_records()

def get_sheet_df(sheet_name):
    data = load_sheet(sheet_name)
    return pd.DataFrame(data)