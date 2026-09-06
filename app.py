import streamlit as st
import plotly.graph_objects as go

from utils.style import apply_theme, COLORS, SCENARIO_LABELS, fmt_rp, fmt_pct
from utils.data_loader import (
    load_summary_kpi,
    load_overview_scenarios,
    load_monthly_trend,
    load_yoy_comparison,
    load_cost_structure,
)

st.set_page_config(
    page_title="Marketplace Store Viability Dashboard 2026",
    layout="wide",
)
apply_theme()

summary = load_summary_kpi().iloc[0]
scenarios = load_overview_scenarios()
monthly = load_monthly_trend()
yoy = load_yoy_comparison()
cost = load_cost_structure()

scenario_pick = {row["scenario"]: row for _, row in scenarios.iterrows()}

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("Marketplace Store Viability Dashboard 2026")
st.caption(
    "Home & kitchenware store on Shopee. Data period: December 2023 to November 2025, "
    "20,848 orders."
)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# The business question
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="biz-card">
        <h4>The question this dashboard answers</h4>
        <p style="font-size:1.1rem; font-weight:600; color:{COLORS['primary_dark']};">
            Is it still worth opening or continuing a store on a marketplace in 2026?
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="biz-card">
        <span class="verdict-label">Viable, with conditions</span>
        <p>
        The store makes money, but not by much, and the margin has been shrinking. Under
        realistic reseller cost assumptions (cost of goods at 55% of the selling price), two
        years of sales produced a net margin of 3.8%. That number only holds up if the store
        keeps its cost of goods under roughly 45 to 50%, stops leaning on its current
        best-sellers (several of which lose money once real shipping and platform fees are
        counted), and plans ahead for higher 2026 platform commissions and the new 0.5% PPh22
        withholding tax.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
st.subheader("Headline numbers (two years, completed orders only)")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total revenue", fmt_rp(summary["total_revenue_rp"]))
k2.metric(
    "Completed orders",
    f"{int(summary['completed_orders']):,}".replace(",", "."),
    f"{summary['completed_pct']:.1f}% of {int(summary['total_orders']):,}".replace(",", "."),
)
k3.metric(
    "Cancellation rate",
    fmt_pct(summary["cancelled_pct"]),
    delta=f"{int(summary['cancelled_orders']):,}".replace(",", ".") + " orders",
    delta_color="inverse",
)
k4.metric("Average order value", fmt_rp(summary["aov_rp"]))

umum = scenario_pick["umum"]
k5.metric(
    "Net margin, typical scenario",
    fmt_pct(umum["margin_pct"]),
    fmt_rp(umum["profit_net_rp"]) + " net profit",
)

st.markdown("###### Net profit by cost-of-goods scenario (two-year total)")
p1, p2, p3 = st.columns(3)
for col, key in zip([p1, p2, p3], ["efisien", "umum", "ketat"]):
    row = scenario_pick[key]
    col.metric(
        SCENARIO_LABELS[key],
        fmt_rp(row["profit_net_rp"]),
        fmt_pct(row["margin_pct"]) + " margin",
        delta_color="normal" if row["profit_net_rp"] >= 0 else "inverse",
    )

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Supporting data: monthly revenue & profit trend
# ---------------------------------------------------------------------------
st.subheader("Revenue and profit over time")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly["Periode"], y=monthly["revenue_rp"],
    name="Revenue", mode="lines", fill="tozeroy",
    line=dict(color=COLORS["accent_light"], width=2),
    fillcolor="rgba(232,175,195,0.35)",
))
fig.add_trace(go.Scatter(
    x=monthly["Periode"], y=monthly["profit_umum_rp"],
    name="Net profit, typical scenario", mode="lines+markers",
    line=dict(color=COLORS["primary"], width=3),
    marker=dict(size=5),
))
fig.update_layout(
    height=380,
    hovermode="x unified",
    yaxis_title="IDR",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Order volume is rising, but revenue and average order value are trending down. "
    "See the Monthly Trends page for the full year-over-year breakdown."
)

# ---------------------------------------------------------------------------
# Supporting data: YoY snapshot
# ---------------------------------------------------------------------------
st.subheader("Year over year, January to November for a fair comparison")

if len(yoy) == 2:
    y24 = yoy[yoy["year"] == 2024].iloc[0] if 2024 in yoy["year"].values else yoy.iloc[0]
    y25 = yoy[yoy["year"] == 2025].iloc[0] if 2025 in yoy["year"].values else yoy.iloc[1]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Orders per month", f"{y25['orders']/11:.0f}", f"{(y25['orders']-y24['orders'])/y24['orders']*100:+.1f}%")
    c2.metric("Annual revenue", fmt_rp(y25["revenue_rp"]), fmt_rp(y25["revenue_rp"]-y24["revenue_rp"]))
    c3.metric("Average order value", fmt_rp(y25["aov_rp"]), fmt_rp(y25["aov_rp"]-y24["aov_rp"]), delta_color="inverse")
    c4.metric(
        "Net profit, typical scenario",
        fmt_rp(y25["profit_umum_rp"]),
        fmt_rp(y25["profit_umum_rp"]-y24["profit_umum_rp"]),
        delta_color="inverse" if y25["profit_umum_rp"] < y24["profit_umum_rp"] else "normal",
    )

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Cost structure snapshot
# ---------------------------------------------------------------------------
st.subheader("Where the revenue goes, typical scenario")

row = cost[cost["scenario"] == "umum"].iloc[0]
labels = ["Cost of goods", "Shipping subsidy", "Other operating costs", "Platform commission", "Order processing fee", "Net profit"]
values = [row["hpp_pct"], row["ongkir_pct"], row["ops_lain_pct"], row["komisi_pct"], row["proses_pct"], row["profit_pct"]]
colors = [COLORS["primary_dark"], COLORS["accent"], COLORS["accent_light"], COLORS["warning"], "#9E5B72", COLORS["positive"]]

fig2 = go.Figure(go.Bar(
    x=values, y=labels, orientation="h",
    marker_color=colors,
    text=[f"{v:.1f}%" for v in values],
    textposition="outside",
))
fig2.update_layout(height=340, xaxis_title="Percent of revenue", showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.write(
    f"The shipping subsidy, meaning the free-shipping cost the store absorbs, comes to "
    f"{row['ongkir_pct']:.1f}% of revenue. That's more than the platform commission itself. "
    "The Cost Structure page has concrete ways to bring that number down."
)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    """
    #### What's on the other pages

    Monthly Trends covers revenue, profit and average order value over time, with
    period filters. Category Breakdown looks at which product categories actually
    make money. Regional Performance shows where orders and revenue are concentrated.
    Cost Structure breaks down the full cost stack and lays out shipping-subsidy
    reduction strategies. Scenario Simulator lets you set your own cost-of-goods and
    shipping-subsidy percentages to test outcomes. Regulations and Assumptions covers
    the 2026 platform fees, the PPh22 tax rule, and the wider market context.
    """
)
