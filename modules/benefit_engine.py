import pandas as pd

from database.google_sheet_solokradjo_one import spreadsheet


def update_benefit(df, periode):
    """
    Mengisi data benefit ke Payroll Workspace
    """

    benefit_sheet = spreadsheet.worksheet("BENEFIT")
    benefit_data = benefit_sheet.get_all_records()

    print(benefit_data[:3])

    benefit_df = pd.DataFrame(benefit_data)

    print("===== BENEFIT ASLI =====")
    print(benefit_df.head())

    print("PERIODE:")
    print(benefit_df["PERIODE"].unique())

    print("NAMA:")
    print(benefit_df["NAMA KARYAWAN"].tolist())




    # ==========================================
    # FILTER PERIODE
    # ==========================================

    benefit_df = benefit_df[
        benefit_df["PERIODE"].astype(str).str.strip() == periode
    ].copy()

    print("===== SETELAH FILTER =====")
    print(benefit_df.head())

    # ==========================================
    # HAPUS KOLOM PERIODE
    # ==========================================

    benefit_df = benefit_df.drop(columns=["PERIODE"])

    print(benefit_df[["BONUS",
    "TUNJANGAN JABATAN", "TUNJANGAN KINERJA"]].head())

    # ==========================================
    # UBAH KOLOM ANGKA
    # ==========================================

    kolom_angka = [
        "BONUS",
        "TUNJANGAN JABATAN",
        "TUNJANGAN KINERJA",
        "TUNJANGAN PENDIDIKAN ANAK",
        "BPJS KES KARYAWAN",
        "BPJS TK KARYAWAN",
        "BPJS KES PERUSAHAAN",
        "BPJS TK PERUSAHAAN",
        "TUNJANGAN MAKAN MINUM"
    ]

    for kolom in kolom_angka:

        if kolom in benefit_df.columns:

            benefit_df[kolom] = pd.to_numeric(
                benefit_df[kolom],
                errors="coerce"
            ).fillna(0)

            benefit_df[kolom] = benefit_df[kolom] * 1000

    # ==========================================
    # MERGE
    # ==========================================

    print(benefit_df.columns.tolist())
    benefit_df = benefit_df[
            [
                "NAMA KARYAWAN",
                "BONUS",
                "TUNJANGAN JABATAN",
                "TUNJANGAN KINERJA",
                "TUNJANGAN PENDIDIKAN ANAK",
                "BPJS KES KARYAWAN",
                "BPJS TK KARYAWAN",
                "BPJS KES PERUSAHAAN",
                "BPJS TK PERUSAHAAN",
                "TUNJANGAN MAKAN MINUM",
                "TEMPAT TINGGAL"
            ]
    ]
    
    df = df.merge(
        benefit_df,
        how="left",
        on="NAMA KARYAWAN"
    )

    # ==========================================
    # ISI NULL
    # ==========================================

    for kolom in kolom_angka:

        if kolom in df.columns:

            df[kolom] = df[kolom].fillna(0)

    if "TEMPAT TINGGAL" in df.columns:

        df["TEMPAT TINGGAL"] = df["TEMPAT TINGGAL"].fillna("")

    return df