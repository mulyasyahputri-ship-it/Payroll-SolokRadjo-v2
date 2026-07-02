import streamlit as st
import pandas as pd

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from utils.utils import rupiah, to_int

from database.google_sheet_solokradjo_one import get_sheet_df
from utils.utils import rupiah


df = get_sheet_df("PAYROLL")

df.columns = df.columns.str.strip()

st.title("🧾 Slip Gaji")

periode = st.selectbox(
    "Pilih Periode",
    sorted(df["PERIODE"].unique(), reverse=True)
)


nama = st.selectbox(
    "Pilih Karyawan",
    sorted(
        df[df["PERIODE"] == periode]["NAMA KARYAWAN"].unique()
    )
)

row = df[
    (df["PERIODE"] == periode) &
    (df["NAMA KARYAWAN"] == nama)
].iloc[0]


nama = row["NAMA KARYAWAN"]
unit = row["NAMA UNIT"]
jabatan = row["JABATAN"]
periode_pdf = row["PERIODE"]

gaji_pokok = to_int(row["GAJI POKOK"])
tunjangan_jabatan = to_int(row["TUNJANGAN JABATAN"])
tunjangan_kinerja = to_int(row["TUNJANGAN KINERJA"])
tunjangan_pendidikan = to_int(row["TUNJANGAN PENDIDIKAN ANAK"])
upah_lembur = to_int(row["UPAH LEMBUR"])
bonus = to_int(row["BONUS"])

total_penerimaan = to_int(row["TOTAL PENERIMAAN"])

saldo_pinjaman = to_int(row["SALDO PINJAMAN"])
cicilan = to_int(row["CICILAN"])
sisa_pinjaman = to_int(row["SISA PINJAMAN"])

bpjs_kes = to_int(row["BPJS KES KARYAWAN"])
bpjs_tk = to_int(row["BPJS TK KARYAWAN"])

total_pengurangan = to_int(row["TOTAL PENGURANGAN"])
gaji_diterima = to_int(row["GAJI DITERIMA"])

tunjangan_makan = to_int(row["TUNJANGAN MAKAN MINUM"])
bpjs_kes_perusahaan = to_int(row["BPJS KES PERUSAHAAN"])
bpjs_tk_perusahaan = to_int(row["BPJS TK PERUSAHAAN"])
tempat_tinggal = to_int(row["TEMPAT TINGGAL"])

jumlah_benefit = to_int(row["JUMLAH BENEFIT"])
total_gaji_benefit = to_int(row["TOTAL GAJI & BENEFIT"])

col1, col2 = st.columns([2,2])

with col1:
    st.markdown("""
### KPSU SOLOK RADJO

Nagari Aie Dingin

Kabupaten Solok

www.solokradjo.org
""")

with col2:
    st.write(f"**Unit Kerja :** {unit}")
    st.write(f"**Nama :** {nama}")
    st.write(f"**Jabatan :** {jabatan}")
    st.write(f"**Periode :** {periode_pdf}")

pendapatan = pd.DataFrame({
    "Keterangan":[
        "Gaji Pokok",
        "Tunjangan Jabatan",
        "Tunjangan Kinerja",
        "Tunjangan Pendidikan Anak",
        "Upah Lembur",
        "Bonus",
        "Total Penerimaan"
    ],
    "Nominal":[
        rupiah(gaji_pokok),
        rupiah(tunjangan_jabatan),
        rupiah(tunjangan_kinerja),
        rupiah(tunjangan_pendidikan),
        rupiah(upah_lembur),
        rupiah(bonus),
        rupiah(total_penerimaan)
    ]
})


potongan = pd.DataFrame({
    "Keterangan":[
        "Bayar Pinjaman",
        "BPJS TK",
        "BPJS Kesehatan",
        "Pengurangan Lain",
        "TOTAL PENGURANGAN"
    ],
    "Nominal":[
        rupiah(cicilan),
        rupiah(bpjs_tk),
        rupiah(bpjs_kes),
        rupiah(total_pengurangan - cicilan - bpjs_tk - bpjs_kes),
        rupiah(total_pengurangan)
    ]
})

pinjaman = pd.DataFrame({
    "Keterangan":[
        "Saldo Pinjaman",
        "Sisa Pinjaman"
    ],
    "Nominal":[
        rupiah(saldo_pinjaman),
        rupiah(sisa_pinjaman)
    ]
})


benefit = pd.DataFrame({
    "Benefit":[
        "Tunjangan Makan Minum",
        "BPJS Kesehatan Perusahaan",
        "BPJS TK Perusahaan",
        "Tempat Tinggal",
        "TOTAL BENEFIT"
    ],
    "Nominal":[
        rupiah(tunjangan_makan),
        rupiah(bpjs_kes_perusahaan),
        rupiah(bpjs_tk_perusahaan),
        rupiah(tempat_tinggal),
        rupiah(jumlah_benefit)
    ]
})

st.table(pinjaman)

kiri, kanan = st.columns(2)

with kiri:
    st.table(pendapatan)

with kanan:
    st.table(potongan)

st.metric(
    "GAJI DITERIMA",
    rupiah(gaji_diterima)
)

st.table(benefit)

st.metric(
    "TOTAL GAJI + BENEFIT",
    rupiah(total_gaji_benefit)
)

logo = ImageReader("assets/logo_solokradjo.png")
if st.button("📄 Generate PDF"):
    pdf = canvas.Canvas(f"Slip_Gaji_{nama}.pdf", pagesize=A4
                        )
    pdf.drawImage(logo, 50, 725, width=65,height=65)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(275, 660, "SLIP GAJI")
        
    pdf.setFont("Helvetica", 12)
    pdf.drawString(120, 775, "KPSU SOLOK RADJO")
    pdf.setFont("Helvetica",9)
    pdf.drawString(120, 755, "Nagari Aie Dingin")
    pdf.drawString(120, 740, "Kabupaten Solok")
    pdf.drawString(120,725, "www.solokradjo.org")
        
    pdf.line(50, 645, 550, 645)
        
    pdf.setFont("Helvetica", 10)
        
    pdf.drawString(360,775,"Unit Kerja")
        
    pdf.drawString(450,775,f": {unit}")

    pdf.drawString(360,755,"Nama")
    pdf.drawString(450,755,f": {nama}")

    pdf.drawString(360,735, "Jabatan")
    pdf.drawString(450,735,f": {jabatan}")

    pdf.drawString(360,715,"Periode")
    pdf.drawString(450,715,": Juni 2026")

    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(50,620, "PENERIMAAN")
    pdf.drawString(320,620,"POTONGAN")

    pdf.line(50, 610,310,610)
    pdf.line(320,610,550,610)

    pdf.setFont("Helvetica", 10)

    pdf.drawString(320,585, "Bayar Pinjaman")
    pdf.drawRightString(530,585, rupiah(cicilan))

    pdf.drawString(320,565,"Kasbon")
    pdf.drawRightString(530,565, "Rp 0")

    pdf.drawString(320,545,"Sisa Pinjaman")
    pdf.drawRightString(530,545, rupiah(sisa_pinjaman))

    pdf.drawString(320,505,"BPJS TK JHT")
    pdf.drawRightString(530,505, rupiah(bpjs_tk))

    pdf.drawString(320,485, "BPJS KESEHATAN")
    pdf.drawRightString(530,485, rupiah(bpjs_kes))

    pdf.drawString(320,465,"Pembayaran Kasbon")
    pdf.drawRightString(530,465, "Rp 0")

    pdf.line(320,445,550,445)

    pdf.setFont("Helvetica-Bold",10)

    pdf.drawString(320,425,"TOTAL POTONGAN")
    pdf.drawRightString(530,425, rupiah(total_pengurangan))

    pdf.drawString(50,585,"Gaji Pokok")
    pdf.drawRightString(300,585,rupiah(gaji_pokok))

    pdf.drawString(50,565,"Tunjangan Jabatan")
    pdf.drawRightString(300,565,rupiah(tunjangan_jabatan))

    pdf.drawString(50,545, "Tunjangan Kinerja")
    pdf.drawRightString(300, 545, rupiah(tunjangan_kinerja))

    pdf.drawString(50,525,"Lembur")
    pdf.drawRightString(300, 525, rupiah(upah_lembur))

    pdf.drawString(50,505,"Bonus")
    pdf.drawRightString(300,505, rupiah(bonus))

    pdf.line(50,485,310,485)

    pdf.setFont("Helvetica-Bold", 10)
                
    pdf.drawString(50, 465, "TOTAL PENERIMAAN")
    pdf.drawRightString(300,465,rupiah(total_penerimaan))

    pdf.setLineWidth(1.5)
    pdf.rect(50,370,230,30)

    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(60,382, "GAJI DITERIMA")

    pdf.drawRightString(
        260,
        382,
        rupiah("gaji_diterima")
    )

    pdf.setFont("Helvetica-Bold",10)
    pdf.drawString(50,330,"BENEFIT :")

    pdf.setFont("Helvetica-Bold",9)

    pdf.drawString(50,310,"BPJS TK JHT")
    pdf.drawString(50,290,"BPJS KESEHATAN")
    pdf.drawString(50,270,"Tunjangan Makan")

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(320,330,"CATATAN")

    pdf.setFont("Helvetica", 9)

    pdf.drawString(320,310,"Tujuan dan bonus dapat berubah")
    pdf.drawString(320,295,"sewaktu-waktu tergantung")
    pdf.drawString(320,280, "kinerja dan capaian penjualan")
    pdf.drawString(320,265,"setiap bulan.")


    pdf.setFont("Helvetica", 10)

    pdf.drawString(70,220, "Dibuat Oleh")

    pdf.drawString(370,220, "Diterima Oleh")

    pdf.line(50,170,180,170)
    pdf.line(320,170,500,170)

    pdf.drawString(90, 155, "Finance")

    pdf.drawString(390,155,nama)

    pdf.save()
