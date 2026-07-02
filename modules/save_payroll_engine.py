import pandas as pd

from database.google_sheet_solokradjo_one import spreadsheet


def save_payroll(df_update, periode):

    worksheet = spreadsheet.worksheet("PAYROLL_INPUT")

    # ==========================
    # COPY DATA
    # ==========================

    df_update = df_update.copy()

    # ==========================
    # LOAD SELURUH PAYROLL_INPUT
    # ==========================

    data = worksheet.get_all_records()

    df_all = pd.DataFrame(data)

    # ==========================
    # GABUNGKAN DENGAN PERIODE LAIN
    # ==========================

    if df_all.empty:

        df_final = df_update

    else:

        df_lain = df_all[
            df_all["PERIODE"] != periode
        ]

        df_final = pd.concat(
            [df_lain, df_update],
            ignore_index=True
        )

    # ==========================
    # BERSIHKAN DATA
    # ==========================

    df_final = df_final.fillna("")
    df_final = df_final.replace({pd.NA: ""})

    # ==========================
    # SIMPAN KE GOOGLE SHEET
    # ==========================

    try:

        worksheet.clear()

        worksheet.update(
            [df_final.columns.tolist()]
            + df_final.values.tolist()
        )

    except Exception as e:

        print("ERROR SAVE PAYROLL :", e)
        raise

    return df_final