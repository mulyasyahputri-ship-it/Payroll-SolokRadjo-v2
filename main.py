PERIODE = input("Masuk periode (YYYY-MM): ").strip()

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from datetime import datetime
try:
    datetime.strptime(PERIODE, "%Y-%m")
except ValueError:
    print("Format periode harus YYYY-MM, contoh: 2026-06")
    exit()

import gspread
 
import os

def to_int(nilai):
    if not nilai:
        return 0
    
    return int(
        str(nilai)
        .replace("Rp", "")
        .replace("rp", "")
        .replace(".", "")
        .replace(" ", "")

    )

print(os.getcwd())
print(os.listdir())

print("=" *50)
print(f" MEMULAI PROSES PAYROLL {PERIODE}")
print("=" *50)

gc = gspread.service_account(
    filename=r"C:\Users\mulya\OneDrive\Desktop\Payroll_SolokRadjo\msp-payroll-system-6caa7172d0c4.json"
)

spreadsheet = gc.open("MSP_PAYROLL_DATABASE")

print("Membaca data karyawan...")
karyawan_sheet = spreadsheet.worksheet("KARYAWAN")
print("Membaca data absensi...")
absensi_sheet = spreadsheet.worksheet("ABSENSI")
print("Membaca data hutang...")
hutang_sheet = spreadsheet.worksheet("HUTANG")
print("Membaca data benefit...")
benefit_sheet = spreadsheet.worksheet("BENEFIT")
payroll_sheet = spreadsheet.worksheet("PAYROLL")

karyawan_data = karyawan_sheet.get_all_records()
absensi_data = absensi_sheet.get_all_records()
hutang_data = hutang_sheet.get_all_records()
benefit_data = benefit_sheet.get_all_records()

print("JUMLAH BARIS HUTANG:", 
      len(hutang_data))
print(hutang_data)

hutang_lookup={}
hutang_update=[]

for i, row in enumerate(hutang_data, start=2):
    print(row)

    print("ISI HUTANG LOOKUP")
    print(hutang_lookup)

    if row["PERIODE"] != PERIODE : continue
    nama = row["Nama"]
    periode_terakhir = row["Periode Terakhir Dipotong"]
    cicilan = to_int(row["Cicilan/Bulan"])

    total_hutang = to_int(row["Total Hutang"])
    sisa_hutang = to_int(row["Sisa Hutang"])

    if periode_terakhir == PERIODE:
        hutang_lookup[nama] = {
        "saldo": 0,
        "bayar": 0,
        "sisa" : 0
        }
        continue


    if sisa_hutang == 0:
        sisa_hutang = total_hutang
    
    sisa_baru = max(0, sisa_hutang -
                    cicilan)
    
    hutang_lookup[nama] = {
        "saldo": sisa_hutang,
        "bayar": cicilan,
        "sisa": sisa_baru
    }

    if sisa_baru == 0:
        status = "Lunas"
    else:
        status = "Berjalan"
    
    hutang_update.append({
        "row": i,
        "sisa": sisa_baru,
        "status": status,
        "periode": PERIODE
    })

for item in hutang_update:
    hutang_sheet.update(
        f"G{item['row']}",
        [[item["sisa"]]]
    )

    hutang_sheet.update(
        f"I{item['row']}",
       [[item["status"]]]
    )

    hutang_sheet.update(
        f"H{item['row']}",
        [[item["periode"]]]
    )

print("="*50)
print("HUTANG LOOKUP FINAL")
print(hutang_lookup)
print("="*50)

absensi_lookup = {}

for row in absensi_data:

    date = datetime.strptime(row["Date"], "%m/%d/%Y")

    print(date.strftime("%Y-%m"), PERIODE)

    if date.strftime("%Y-%m") != PERIODE: continue


    nama = row["Nama Karyawan"]

    if nama not in absensi_lookup:
        absensi_lookup[nama] ={
            "hari_kerja" : 0,
            "total_jam": 0,
            "total_lembur": 0,
        }
    if row["Check In"] and row ["Check Out"] :
        absensi_lookup[nama] ["hari_kerja"] += 1

        try: masuk = datetime.strptime(str(row["Check In"]), 
                                  "%H:%M:%S") 
        except: masuk = datetime.strptime(str(row["Check In"]), "%H:%M")

        try: pulang = datetime.strptime(str(row["Check Out"]), 
                                   "%H:%M:%S") 
        except: pulang = datetime.strptime(str(row["Check Out"]), "%H:%M")
    
        jam_kerja = (pulang -masuk).total_seconds() /3600

        JAM_NORMAL = 9

        if jam_kerja > JAM_NORMAL:
            lembur = jam_kerja - JAM_NORMAL
        else:
            lembur = 0
        
        absensi_lookup[nama] ["total_lembur"] += lembur
        absensi_lookup[nama] ["total_jam"] += jam_kerja
    
print(absensi_lookup)

for nama in absensi_lookup:
    total_lembur = absensi_lookup[nama] ["total_lembur"]
    upah_lembur = round(total_lembur * 10000)
    absensi_lookup[nama] ["upah_lembur"] = upah_lembur

print(absensi_lookup)

benefit_lookup = {}

for row in benefit_data :

    if row["PERIODE"] != PERIODE : continue
    nama = row["NAMA"]

    benefit_lookup[nama] = {
        "bonus": 
        to_int(row["BONUS"] or 0),
        "tunjangan_jabatan": 
        to_int(row["TUNJANGAN JABATAN"] or 0),
        "tunjangan_kinerja": 
        to_int(row["TUNJANGAN KINERJA"] or 0),
        "tunjangan_anak": 
        to_int(row["TUNJANGAN PENDIDIKAN ANAK"] or 0),
        "bpjs_kes_karyawan":
        to_int(row["BPJS KESEHATAN KARYAWAN"] or 0),
        "bpjs_tk_karyawan":
        to_int(row["BPJS TK KARYAWAN"] or 0),
        "bpjs_kes" : 
        to_int(row["BPJS KESEHATAN PERUSAHAAN"] or 0),
        "bpjs_tk": 
        to_int(row["BPJS TK PERUSAHAAN"] or 0),
        "tunjangan_makan": 
        to_int(row["TUNJANGAN MAKAN MINUM"] or 0),
        "tempat_tinggal": 
        to_int(row["TEMPAT TINGGAL"] or 0)

    }

    hasil_payroll = []

for karyawan in karyawan_data :

    nama = karyawan["Nama Karyawan"]
    gaji_pokok = int(
        str(karyawan["Gaji Pokok"]) 
    .replace(".", "") 
    .replace(".", "")
    )
    pinjaman = hutang_lookup.get(nama, {})

    saldo_pinjaman = pinjaman.get("saldo", 0)
    bayar_pinjaman = pinjaman.get("bayar", 0)
    sisa_pinjaman = pinjaman.get("sisa", 0)

    potongan_hutang = bayar_pinjaman

    absen = absensi_lookup.get(nama,{})
    benefit  = benefit_lookup.get(nama, {})
    bonus = benefit.get("bonus", 0)
    tunjangan_jabatan = benefit.get("tunjangan_jabatan", 0)
    tunjangan_kinerja = benefit.get("tunjangan_kinerja", 0)
    tunjangan_anak = benefit.get("tunjangan_anak", 0)
    bpjs_kes = benefit.get("bpjs_kes", 0)
    bpjs_tk = benefit.get("bpjs_tk", 0)
    bpjs_kes_karyawan = benefit.get("bpjs_kes_karyawan", 0)
    bpjs_tk_karyawan = benefit.get("bpjs_tk_karyawan", 0)
    tunjangan_makan = benefit.get("tunjangan_makan", 0)
    tempat_tinggal = benefit.get("tempat_tinggal", 0)
    hari_kerja = absen.get("hari_kerja", 0)
    total_jam = absen.get("total_jam", 0)
    total_lembur = absen.get("total_lembur", 0)
    upah_lembur = absen.get("upah_lembur", 0)

    potongan_bpjs = (
        bpjs_kes_karyawan
        + bpjs_tk_karyawan
    )

    total_penerimaan = ( gaji_pokok
                   + tunjangan_jabatan
                   + tunjangan_kinerja
                   + tunjangan_anak
                   + upah_lembur
                   + bonus
                   )
    
    total_potongan = (
        potongan_hutang
        + potongan_bpjs
    )
   
    gaji_bersih = (
        total_penerimaan
        - total_potongan
    )

    jumlah_benefit = (
        bpjs_kes
        + bpjs_tk
        + tunjangan_makan
        + tempat_tinggal
    )

    total_gaji_benefit = (
        gaji_bersih
        + jumlah_benefit
    )

    hasil_payroll.append([
        "", # NO (kosong dulu)
        PERIODE,
        nama,
        karyawan["Nama Unit"],
        karyawan["Jabatan"],
        gaji_pokok,
        tunjangan_jabatan,
        tunjangan_kinerja,
        tunjangan_anak,
        upah_lembur,
        bonus,
        total_penerimaan,
        saldo_pinjaman,
        potongan_hutang, # atau bayar_pinjaman
        bayar_pinjaman, 
        sisa_pinjaman,
        bpjs_kes_karyawan,
        bpjs_tk_karyawan,
        total_potongan,
        gaji_bersih,
        tunjangan_makan,
        bpjs_kes,
        bpjs_tk,
        tempat_tinggal,
        jumlah_benefit,
        total_gaji_benefit
    ])

    print("="*40)
    print("Nama :", nama)
    print("Gaji Pokok :", gaji_pokok)
    print("Hari Kerja :", hari_kerja)
    print("Total Jam :", round(total_jam,2)) 
    print("Total Lembur :", round(total_lembur, 2))
    print("Upah Lembur :", upah_lembur)

    print("Bonus :", bonus)
    print("Tunjangan Jabatan :", tunjangan_jabatan)
    print("Tunjangan Kinerja :", tunjangan_kinerja)
    print("Tunjangan Anak :", tunjangan_anak)

    print("BPJS Kes (Perusahaan) :", bpjs_kes)
    print("BPJS TK (Perusahaan) :", bpjs_tk)
    print("Tunjangan Makan :", tunjangan_makan)
    print("Tempat Tinggal :", tempat_tinggal)

    print("Jumlah Benefit :", jumlah_benefit)
    print("Potongan Hutang :", potongan_hutang)
    print("Gaji Bersih :", gaji_bersih)
    print("Total Gaji + Benefit :", total_gaji_benefit)

payroll_sheet.batch_clear(["A2:Z"])
payroll_sheet.append_rows(hasil_payroll)

print("Payroll berhasil dibuat!")

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

def rupiah(nilai) :
    return f"Rp{nilai:,.0f}".replace(",", ".")

import os

os.makedirs("Slip Gaji",
            exist_ok=True)

for data in hasil_payroll:
    periode = data [1]
    nama = data[2]
    unit = data [3]
    jabatan = data [4]
    gaji_pokok = data [5]
    tunjangan_jabatan = data [6]
    tunjangan_kinerja = data [7]
    tunjangan_anak = data [8]
    upah_lembur = data [9]
    bonus = data [10]
    total_penerimaan = data [11]

    saldo_pinjaman = data [12]
    pinjaman_berjalan = data [13]
    bayar = data[14]
    sisa_pinjaman =  data [15]

    bpjs_kes_karyawan = data[16]
    bpjs_tk_karyawan = data[17]
    total_potongan = data [18]
    gaji_bersih = data[19]

    tunjangan_makanan = data[20]
    bpjs_kes = data [21]
    bpjs_tk = data [22]
    tempat_tinggal = [23]
    jumlah_benefit = [24]
    total_gaji_benefit = data [25]

 # seluruh kode pembuat PDF
    
    print(nama)
    print(total_penerimaan)
    logo = ImageReader("logo_solokradjo.png")
    pdf = canvas.Canvas(f"Slip_Gaji_{nama}.pdf", pagesize=A4
                        )
    pdf.drawImage("logo_solokradjo.png", 50, 725, width=65,height=65)
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
    pdf.drawRightString(530,585, rupiah(bayar))

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
    pdf.drawRightString(530,425, rupiah(total_potongan))

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
        rupiah(gaji_bersih)
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

    print("PDF berhasil dibuat")


