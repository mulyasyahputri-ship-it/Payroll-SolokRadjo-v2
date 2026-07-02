import pandas as pd

from database.google_sheet_solokradjo_one import spreadsheet


# ==========================================
# UPDATE HUTANG
# ==========================================

def update_hutang(df, periode):
    """
    Mengisi data hutang ke Payroll Workspace
    """

    # ==========================================
    # LOAD HUTANG
    # ==========================================

    hutang_sheet = spreadsheet.worksheet("HUTANG")
    hutang_data = hutang_sheet.get_all_records() 
    print(hutang_data)

    for row in hutang_data:
        print(row["NAMA KARYAWAN"],
              row["SALDO PINJAMAN"],
              type(row["SALDO PINJAMAN"]))
        print(row["CICILAN"],
              type(row["CICILAN"]))
        

    hutang_df = pd.DataFrame(hutang_data)

    print(
        hutang_df[
            [
                "NAMA KARYAWAN",
                "SALDO PINJAMAN"
            ]
        ]
    )

    print(hutang_df["SALDO PINJAMAN"].apply(type))

    # ==========================================
    # FILTER PERIODE
    # ==========================================

    hutang_df = hutang_df[
        hutang_df["PERIODE"].astype(str).str.strip() == periode
    ]

    print(hutang_df)
    print(hutang_data)

    # ==========================================
    # HAPUS KOLOM YANG TIDAK DIPERLUKAN
    # ==========================================

    kolom_dipakai = [
        "NAMA KARYAWAN",
        "SALDO PINJAMAN",
        "CICILAN",
        "SISA PINJAMAN"
    ]

    hutang_df = hutang_df[kolom_dipakai]

    # ==========================================
    # UBAH KE ANGKA
    # ==========================================

    kolom_angka = [
        "SALDO PINJAMAN",
        "CICILAN",
        "SISA PINJAMAN"
    ]

    print(
        hutang_df[
            [
                "NAMA KARYAWAN",
                "SALDO PINJAMAN",
                "CICILAN",
                "SISA PINJAMAN"
            ]
        ]
    )

    for kolom in kolom_angka:

        if kolom in hutang_df.columns:

            hutang_df[kolom] = hutang_df[kolom].apply(
                lambda x: str(x).replace(".", "") if isinstance(x, str) else x
                )
            hutang_df[kolom] = pd.to_numeric(
            hutang_df[kolom],
            errors="coerce"
            ).fillna(0)
            
            hutang_df[kolom] = hutang_df[kolom].apply(
                lambda x: x * 1000 if 0 < x < 1000 else x
                  ).astype(int)

    # ==========================================
    # MERGE
    # ==========================================

    df = df.merge(
        hutang_df,
        how="left",
        on="NAMA KARYAWAN"
    )

    # ==========================================
    # ISI NILAI KOSONG
    # ==========================================

    for kolom in kolom_angka:

        if kolom in df.columns:

            df[kolom] = (
                pd.to_numeric(
                    df[kolom],
                    errors="coerce"
                )
                .fillna(0)
                .astype(int)
            )

    return df