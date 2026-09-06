"""
Centralized, cached data loading for the dashboard.
All figures are pre-aggregated from the source workbook at build time
(see prep_data.py) and shipped as CSVs in /data for fast Streamlit Cloud
cold starts.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def load_summary_kpi() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "summary_kpi.csv")


@st.cache_data
def load_overview_scenarios() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "overview_scenarios.csv")


@st.cache_data
def load_monthly_trend() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "monthly_trend.csv")
    df["Periode"] = pd.to_datetime(df["Periode"], format="%Y-%m")
    return df.sort_values("Periode")


@st.cache_data
def load_category_breakdown() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "category_breakdown.csv")


@st.cache_data
def load_region_breakdown() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "region_breakdown.csv")


@st.cache_data
def load_city_top30() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "city_top30.csv")


@st.cache_data
def load_cost_structure() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "cost_structure.csv")


@st.cache_data
def load_payment_method() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "payment_method.csv")


@st.cache_data
def load_shipping_option() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "shipping_option.csv")


@st.cache_data
def load_yoy_comparison() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "yoy_comparison.csv")


@st.cache_data
def load_transactions() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "transactions_completed.csv")
    return df


@st.cache_data
def load_dim_kategori_tarif() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "dim_kategori_tarif.csv")


@st.cache_data
def load_dim_asumsi_hpp() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "dim_asumsi_hpp.csv")


@st.cache_data
def load_dim_biaya_operasional() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "dim_biaya_operasional.csv")


@st.cache_data
def load_dim_data_makro() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "dim_data_makro.csv")


@st.cache_data
def load_dim_biaya_platform() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "dim_biaya_platform.csv")


@st.cache_data
def load_dim_pajak_pph22() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "dim_pajak_pph22.csv")
