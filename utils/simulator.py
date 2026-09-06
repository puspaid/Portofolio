"""
Custom scenario calculator: lets the user override the COGS % and the
free-shipping subsidy % to see the effect on net profit, using the same
real transaction-level revenue, platform commission and processing-fee
figures already computed in the source data.
"""

import pandas as pd


def simulate(
    df: pd.DataFrame,
    cogs_pct: float,
    ongkir_pct: float,
    ops_lain_pct: float,
) -> dict:
    """
    df: transactions_completed dataframe with real 'Total Pembayaran',
        'Estimasi_Biaya_Komisi_Rp', 'Estimasi_Biaya_Proses_Pesanan_Rp'.
    cogs_pct, ongkir_pct, ops_lain_pct: user-controlled percentages (0-100)
        applied uniformly on top of revenue, replacing the fixed scenario
        assumptions used elsewhere in the dashboard.
    """
    revenue = df["Total Pembayaran"].sum()
    komisi = df["Estimasi_Biaya_Komisi_Rp"].sum()
    proses = df["Estimasi_Biaya_Proses_Pesanan_Rp"].sum()

    cogs_rp = revenue * (cogs_pct / 100)
    ongkir_rp = revenue * (ongkir_pct / 100)
    ops_lain_rp = revenue * (ops_lain_pct / 100)

    total_cost = cogs_rp + ongkir_rp + ops_lain_rp + komisi + proses
    profit = revenue - total_cost
    margin = (profit / revenue * 100) if revenue else 0

    return {
        "revenue": revenue,
        "cogs_rp": cogs_rp,
        "ongkir_rp": ongkir_rp,
        "ops_lain_rp": ops_lain_rp,
        "komisi_rp": komisi,
        "proses_rp": proses,
        "profit_rp": profit,
        "margin_pct": margin,
    }
