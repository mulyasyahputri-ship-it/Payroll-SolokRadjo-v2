import streamlit as st

from modules.merge_engine import merge_payroll
from modules.payroll_engine import calculate_payroll
from utils.utils import format_rupiah
from modules.approve_payroll_engine import approve_payroll

# nanti
# from modules.approval_engine import approve_payroll


st.title("Payroll Workspace")


# ==========================================
# FILTER
# ==========================================

periode = st.text_input(
    "Periode",
    value="2026-06"
)

unit = st.selectbox(
    "Nama Unit",
    [
        "Semua",
        "01_RETAIL&ROASTERY",
        "02_KPSUSORA",
        "03_MUARO",
        "04_PAYAKUMBUAH",
        "05_GRAMEDIA",
        "06_PINTUANGIN",
        "07_PABRIK KOPI SR",
        "08_TERSBIM"
    ]
)


# ==========================================
# LOAD PAYROLL
# ==========================================

merged_df = merge_payroll(
    periode,
    unit
)

merged_df = calculate_payroll(
    merged_df,
    periode
)

merged_df = merged_df.drop(
      columns=[
            "JUMLAH HUTANG",
            "PINJAMANN"
      ],
      errors="ignore"
)

edited_df = st.dataframe(
    merged_df,
    use_container_width=True,
)


# ==========================================
# BUTTONS
# ==========================================

col1, col2 = st.columns(2)

  
# --------------------
# APPROVE
# --------------------

with col2:

    if st.button("✅ Approve Payroll", use_container_width=True):

            approve_payroll(
                merged_df,
                periode
            )

            st.success("Payroll berhasil diapprove.")