import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard MSP Payroll")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jumlah Karyawan", "0")

with col2:
    st.metric("Hadir Hari Ini", "0")

with col3:
    st.metric("Terlambat", "0")

with col4:
    st.metric("Payroll Bulan Ini", "Rp 0")

st.divider()

st.subheader("Menu Cepat")

c1, c2, c3 = st.columns(3)

with c1:
    st.button("👥 Data Karyawan", use_container_width=True)

with c2:
    st.button("🕒 Input Absensi", use_container_width=True)

with c3:
    st.button("💰 Hitung Payroll", use_container_width=True)

st.divider()

st.subheader("Aktivitas Terbaru")

st.info("Belum ada aktivitas.")