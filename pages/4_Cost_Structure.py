import streamlit as st
import plotly.graph_objects as go

from utils.style import apply_theme, COLORS, SCENARIO_LABELS, fmt_rp, fmt_pct
from utils.data_loader import load_cost_structure, load_payment_method, load_shipping_option

st.set_page_config(page_title="Cost Structure", layout="wide")
apply_theme()

st.title("Cost Structure")
st.caption("Where every rupiah of revenue goes, and how to reduce the shipping subsidy.")

cost = load_cost_structure()
payment = load_payment_method()
shipping = load_shipping_option()

scenario_key = st.selectbox(
    "Cost-of-goods scenario", ["umum", "efisien", "ketat"],
    format_func=lambda x: SCENARIO_LABELS[x],
)
row = cost[cost["scenario"] == scenario_key].iloc[0]

st.markdown(
    f"""
    <div class="biz-card">
        <h4>Question</h4>
        <p>After cost of goods, what's the single biggest controllable cost, and what can
        realistically be done about it?</p>
        <p style="font-weight:600; color:{COLORS['primary_dark']};">
        The shipping subsidy the store absorbs to offer free shipping comes to
        {row['ongkir_pct']:.1f}% of revenue, more than the platform commission
        ({row['komisi_pct']:.1f}%). Unlike cost of goods, this one is directly controllable
        through store policy. See the strategies below.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns([1, 1])
with c1:
    st.markdown("##### Cost stack as a share of revenue")
    labels = ["Cost of goods", "Shipping subsidy", "Other operating costs", "Platform commission", "Processing fee", "Net profit"]
    values = [row["hpp_pct"], row["ongkir_pct"], row["ops_lain_pct"], row["komisi_pct"], row["proses_pct"], max(row["profit_pct"], 0)]
    colors = [COLORS["primary_dark"], COLORS["accent"], COLORS["accent_light"], COLORS["warning"], "#9E5B72", COLORS["positive"]]
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.5, marker_colors=colors))
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("##### Rupiah value per cost component, two-year total")
    comp_labels = ["Cost of\ngoods", "Shipping\nsubsidy", "Other op.\ncosts", "Commission", "Processing\nfee", "Net profit"]
    comp_values = [row["hpp_rp"], row["ongkir_rp"], row["ops_lain_rp"], row["komisi_rp"], row["proses_rp"], row["profit_rp"]]
    colors2 = [COLORS["primary_dark"], COLORS["accent"], COLORS["accent_light"], COLORS["warning"], "#9E5B72", COLORS["positive"] if row["profit_rp"] >= 0 else COLORS["negative"]]
    fig2 = go.Figure(go.Bar(x=comp_labels, y=comp_values, marker_color=colors2,
                             text=[fmt_rp(v) for v in comp_values], textposition="outside"))
    fig2.update_layout(height=420, yaxis_title="IDR")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown("##### Revenue by payment method")
    fig3 = go.Figure(go.Bar(x=payment["Metode Pembayaran"], y=payment["revenue_rp"], marker_color=COLORS["primary"]))
    fig3.update_layout(height=350, yaxis_title="Revenue (Rp)")
    st.plotly_chart(fig3, use_container_width=True)
with c4:
    st.markdown("##### Shipping subsidy by shipping option")
    fig4 = go.Figure(go.Bar(
        x=shipping["Opsi Pengiriman"], y=shipping["ongkir_ditanggung_toko_rp"], marker_color=COLORS["accent"],
    ))
    fig4.update_layout(height=350, yaxis_title="Shipping subsidy absorbed (Rp)")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("Reducing the free-shipping subsidy")

strategies = [
    ("Raise the free-shipping minimum spend",
     "Set free shipping only above roughly Rp50,000 to Rp75,000 per order. This pushes "
     "average order value up while spreading the shipping cost across a larger order."),
    ("Stop subsidizing categories that already lose money",
     "Aksesoris Pintu, Mangkok Sambal and Celengan lose money once realistic cost of goods "
     "is applied. Remove or reduce free shipping on these, or raise their price to cover "
     "the subsidy."),
    ("Bundle small items into single packages",
     "Combining several small SKUs into one parcel lowers shipping cost per rupiah of "
     "revenue, since shipping is billed by package and weight, not by SKU."),
    ("Default to economy courier options",
     "Nudging buyers toward cargo or economy shipping instead of instant or same-day "
     "options avoids the higher rates that are usually subsidized more heavily."),
    ("Use the platform's own shipping-subsidy programs",
     "Programs like Shopee's Gratis Ongkir Xtra shift part of the subsidy to the platform "
     "instead of the store carrying all of it. Worth checking eligibility."),
    ("Cut packaging weight and dimensions",
     "Shipping tariffs are based on volumetric weight, so trimming excess bubble wrap or "
     "cardboard can drop a shipment into a cheaper weight tier."),
    ("Concentrate stock near the highest-demand region",
     "Jabodetabek, West Java, Banten and Central Java dominate orders. A warehouse or "
     "dropship point near that cluster lowers the shipping tariff for most orders."),
    ("Track the subsidy ratio as an ongoing number, not a one-time setting",
     "Check the shipping-subsidy-to-revenue ratio per category or SKU regularly instead of "
     "setting a free-shipping policy once and leaving it alone."),
]

for title, desc in strategies:
    st.markdown(
        f"""
        <div class="biz-card">
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("View the underlying cost-structure table, all scenarios"):
    st.dataframe(cost, use_container_width=True, hide_index=True)
