import streamlit as st

from utils.style import apply_theme, COLORS
from utils.data_loader import (
    load_dim_biaya_platform,
    load_dim_pajak_pph22,
    load_dim_data_makro,
    load_dim_asumsi_hpp,
    load_dim_biaya_operasional,
)

st.set_page_config(page_title="Regulations and Assumptions", layout="wide")
apply_theme()

st.title("Regulations, Platform Fees and Assumptions for 2026")
st.caption("The regulatory and market context behind the numbers in this dashboard.")

st.markdown(
    f"""
    <div class="biz-card">
        <h4>Question</h4>
        <p>What's changing in 2026 that could affect the store's viability beyond its own
        sales performance?</p>
        <p style="font-weight:600; color:{COLORS['primary_dark']};">
        Two regulatory changes matter most: Shopee's 2026 commission increase, and the new
        automatic 0.5% PPh22 withholding tax, effective 1 August 2026, once combined annual
        turnover across all channels under one tax ID passes Rp500 million. This store's 2024
        turnover, around Rp545 million, was already near or past that threshold.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Platform fee structure, 2026")
platform = load_dim_biaya_platform()
st.dataframe(
    platform.rename(columns={
        "Platform": "Platform", "Komponen_Biaya": "Fee component", "Persen_Min": "Min percent",
        "Persen_Max": "Max percent", "Biaya_Tetap_Rp": "Fixed fee (Rp)", "Berlaku_Sejak": "Effective from",
        "Catatan": "Note",
    }),
    use_container_width=True, hide_index=True,
)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("PPh22 withholding tax rule, PMK 37/2025")
pph = load_dim_pajak_pph22()
st.dataframe(
    pph.rename(columns={
        "Ketentuan": "Provision", "Nilai": "Value", "Berlaku_Sejak": "Effective from",
        "Dasar_Hukum": "Legal basis", "Catatan": "Note",
    }),
    use_container_width=True, hide_index=True,
)
st.write(
    "The 0.5% is withheld automatically by the platform on gross turnover, not only on the "
    "amount above Rp500 million, and it's aggregated across all marketplaces and offline "
    "sales under one NPWP or NIK."
)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.subheader("Cost-of-goods scenario assumptions")
    st.dataframe(
        load_dim_asumsi_hpp().rename(columns={
            "Skenario": "Scenario", "HPP_persen_dari_Harga_Jual": "Cost of goods, % of price",
            "Setara_Markup_atas_HPP": "Equivalent markup", "Sumber_Acuan": "Reference",
        }),
        use_container_width=True, hide_index=True,
    )
with c2:
    st.subheader("Other operating cost assumptions")
    st.dataframe(
        load_dim_biaya_operasional().rename(columns={
            "Komponen": "Component", "Persen_atau_Nominal": "Value", "Sumber_Acuan": "Reference",
        }),
        use_container_width=True, hide_index=True,
    )

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("Indonesia e-commerce market context")
makro = load_dim_data_makro()
st.dataframe(
    makro.rename(columns={
        "Sumber": "Source", "Periode": "Period", "Indikator": "Indicator",
        "Nilai": "Value", "Satuan": "Unit", "Catatan": "Note",
    }),
    use_container_width=True, hide_index=True,
)
st.write(
    "The national e-commerce market is still growing, up 20.5% year over year in "
    "transaction volume as of Q3 2025, and 42% of Indonesian small businesses now sell "
    "online. At the same time, the average transaction value is declining nationally, "
    "which lines up with this store's own average-order-value trend."
)
