import streamlit as st
import plotly.graph_objects as go

from utils.style import apply_theme, COLORS, fmt_rp, fmt_pct
from utils.data_loader import load_transactions
from utils.simulator import simulate

st.set_page_config(page_title="Scenario Simulator", layout="wide")
apply_theme()

st.title("Scenario Simulator")
st.caption(
    "Adjust cost of goods and shipping-subsidy percentages to see the effect on net "
    "profit, using the real revenue, commission and processing-fee figures from the "
    "two-year transaction data."
)

df = load_transactions()

st.markdown(
    f"""
    <div class="biz-card">
        <h4>Question</h4>
        <p>What combination of cost of goods and shipping subsidy does this store actually
        need to hit to stay profitable at 2026 platform fee levels?</p>
        <p style="font-weight:600; color:{COLORS['primary_dark']};">
        Use the sliders below. At the current real average shipping subsidy, around 21% of
        revenue, cost of goods needs to stay under roughly 45 to 50% for the store to keep a
        positive margin. Cutting the shipping subsidy in half raises that ceiling meaningfully.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
with c1:
    cogs_pct = st.slider("Cost of goods, percent of selling price", 20, 85, 55, step=1)
with c2:
    ongkir_pct = st.slider("Shipping subsidy absorbed, percent of revenue", 0, 35, 21, step=1)
with c3:
    ops_lain_pct = st.slider("Other operating costs, percent of revenue", 0, 20, 8, step=1)

result = simulate(df, cogs_pct, ongkir_pct, ops_lain_pct)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Revenue, two-year actual", fmt_rp(result["revenue"]))
m2.metric("Simulated net profit", fmt_rp(result["profit_rp"]))
m3.metric("Simulated margin", fmt_pct(result["margin_pct"]))
m4.metric("Result", "Profitable" if result["profit_rp"] > 0 else "Loss-making")

st.markdown("##### Simulated cost breakdown")
labels = ["Cost of goods", "Shipping subsidy", "Other operating costs", "Platform commission", "Processing fee", "Net profit"]
values = [result["cogs_rp"], result["ongkir_rp"], result["ops_lain_rp"], result["komisi_rp"], result["proses_rp"], result["profit_rp"]]
colors = [COLORS["primary_dark"], COLORS["accent"], COLORS["accent_light"], COLORS["warning"], "#9E5B72",
          COLORS["positive"] if result["profit_rp"] >= 0 else COLORS["negative"]]
fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors,
                        text=[fmt_rp(v) for v in values], textposition="outside"))
fig.add_hline(y=0, line_color=COLORS["text_muted"], line_width=1)
fig.update_layout(height=420, yaxis_title="IDR, two-year total")
st.plotly_chart(fig, use_container_width=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown("##### Break-even cost of goods")
st.caption("Given the shipping-subsidy and other-cost settings above, what's the highest cost of goods percentage before the store starts losing money?")

lo, hi = 1, 95
for _ in range(50):
    mid = (lo + hi) / 2
    r = simulate(df, mid, ongkir_pct, ops_lain_pct)
    if r["profit_rp"] > 0:
        lo = mid
    else:
        hi = mid
st.success(f"Break-even cost of goods is about {lo:.1f}% of the selling price, given a {ongkir_pct}% shipping subsidy and {ops_lain_pct}% other operating costs.")
