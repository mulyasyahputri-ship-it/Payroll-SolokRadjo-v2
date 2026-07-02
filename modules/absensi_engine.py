import pandas as pd
from datetime import datetime

from database.google_sheet_solokradjo_one import spreadsheet

# ==========================
# KONSTANTA
# ==========================

JAM_NORMAL = 9
UPAH_PER_JAM_LEMBUR = 10000


# ==========================
# UPDATE ABSENSI
# ==========================

def update_absensi(df, periode):

    absensi_sheet = spreadsheet.worksheet("ABSENSI")
    absensi_data = absensi_sheet.get_all_records()

    absensi_lookup = {}

    # ==========================================
    # REKAP ABSENSI
    # ==========================================

    for row in absensi_data:

        try:
            tanggal = datetime.strptime(
                row["DATE"],
                "%m/%d/%Y"
            )
        except:
            continue

        if tanggal.strftime("%Y-%m") != periode:
            continue

        nama = str(
            row["NAMA KARYAWAN"]
        ).strip()

        if nama not in absensi_lookup:

            absensi_lookup[nama] = {
                "hari_kerja": 0,
                "total_jam": 0,
                "total_lembur": 0
            }

        if row["CHECK IN"] and row["CHECK OUT"]:

            absensi_lookup[nama]["hari_kerja"] += 1

            try:
                masuk = datetime.strptime(
                    str(row["CHECK IN"]),
                    "%H:%M:%S"
                )
            except:
                masuk = datetime.strptime(
                    str(row["CHECK IN"]),
                    "%H:%M"
                )

            try:
                pulang = datetime.strptime(
                    str(row["CHECK OUT"]),
                    "%H:%M:%S"
                )
            except:
                pulang = datetime.strptime(
                    str(row["CHECK OUT"]),
                    "%H:%M"
                )

            jam_kerja = (
                pulang - masuk
            ).total_seconds() / 3600

            lembur = max(
                0,
                jam_kerja - JAM_NORMAL
            )

            absensi_lookup[nama]["total_jam"] += jam_kerja
            absensi_lookup[nama]["total_lembur"] += lembur

    # ==========================================
    # HITUNG UPAH LEMBUR
    # ==========================================

    for nama in absensi_lookup:

        total_lembur = absensi_lookup[nama]["total_lembur"]

        absensi_lookup[nama]["upah_lembur"] = round(
            total_lembur * UPAH_PER_JAM_LEMBUR
        )

    # ==========================================
    # UPDATE PAYROLL
    # ==========================================

    for i in df.index:

        nama = str(
            df.loc[i, "NAMA KARYAWAN"]
        ).strip()

        data = absensi_lookup.get(nama)

        if data is None:

            df.loc[i, "TOTAL HARI KERJA"] = 0
            df.loc[i, "TOTAL JAM LEMBUR"] = 0
            df.loc[i, "UPAH LEMBUR"] = 0

        else:

            df.loc[i, "TOTAL HARI KERJA"] = data["hari_kerja"]

            df.loc[i, "TOTAL JAM LEMBUR"] = round(
                data["total_lembur"],
                2
            )

            df.loc[i, "UPAH LEMBUR"] = data["upah_lembur"]

    return df