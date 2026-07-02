import pandas as pd


def calculate_payroll(df, periode):
    """
    Menghitung payroll berdasarkan
    PAYROLL_INPUT.
    """

    df = df.copy()

    # ==========================
    # Refresh Data
    # ==========================


    # ==========================
    # Pastikan kolom angka
    # ==========================

    kolom_angka = [
        "GAJI POKOK",
        "TUNJANGAN JABATAN",
        "TUNJANGAN KINERJA",
        "TUNJANGAN PENDIDIKAN ANAK",
        "UPAH LEMBUR",
        "BONUS",
        "CICILAN",
        "BPJS KES KARYAWAN",
        "BPJS TK KARYAWAN",
        "TUNJANGAN MAKAN MINUM",
        "BPJS KES PERUSAHAAN",
        "BPJS TK PERUSAHAAN",
        "TEMPAT TINGGAL"
    ]

    for kolom in kolom_angka:

        if kolom in df.columns:

            df[kolom] = (
                pd.to_numeric(
                    df[kolom],
                    errors="coerce"
                )
                .fillna(0)
            )

    # ==========================
    # Total Penerimaan
    # ==========================

    print(df[
        ["NAMA KARYAWAN",
        "GAJI POKOK",
        "TUNJANGAN JABATAN",
        "TUNJANGAN KINERJA",
        "TUNJANGAN PENDIDIKAN ANAK",
        "UPAH LEMBUR",
        "BONUS"
        ]
        ].head())

    df["TOTAL PENERIMAAN"] = (

        df["GAJI POKOK"]

        + df["TUNJANGAN JABATAN"]

        + df["TUNJANGAN KINERJA"]

        + df["TUNJANGAN PENDIDIKAN ANAK"]

        + df["UPAH LEMBUR"]

        + df["BONUS"]

    )

    # ==========================
    # Total Pengurangan
    # ==========================

    df["TOTAL PENGURANGAN"] = (

        df["CICILAN"]

        + df["BPJS KES KARYAWAN"]

        + df["BPJS TK KARYAWAN"]

    )

    # ==========================
    # Gaji Diterima
    # ==========================

    df["GAJI DITERIMA"] = (

        df["TOTAL PENERIMAAN"]

        - df["TOTAL PENGURANGAN"]

    )

    # ==========================
    # Jumlah Benefit
    # ==========================

    df["JUMLAH BENEFIT"] = (

        df["TUNJANGAN MAKAN MINUM"]

        + df["BPJS KES PERUSAHAAN"]

        + df["BPJS TK PERUSAHAAN"]

        + df["TEMPAT TINGGAL"]
    )

    # ==========================
    # Total Gaji & Benefit
    # ==========================

    df["TOTAL GAJI & BENEFIT"] = (

        df["GAJI DITERIMA"]

        + df["JUMLAH BENEFIT"]

    )

    # ===========================
    # Informasi Pinjaman
    # ===========================

    df["JUMLAH HUTANNG"] = df["SALDO PINJAMAN"]
    df["PINJAMAN"] = df["SALDO PINJAMAN"]
    df["SISA PINJAMAN"] = df["SISA PINJAMAN"]

    return df
