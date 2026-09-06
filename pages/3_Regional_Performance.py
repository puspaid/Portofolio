import streamlit as st
import plotly.graph_objects as go

from utils.style import apply_theme, COLORS, CATEGORICAL_SEQUENCE, fmt_rp, fmt_pct
from utils.data_loader import load_region_breakdown, load_city_top30

st.set_page_config(page_title="Regional Performance", layout="wide")
apply_theme()

st.title("Regional Performance")
st.caption("Order and revenue concentration by province and city or district.")

region = load_region_breakdown()
city = load_city_top30()

st.markdown(
    f"""
    <div class="biz-card">
        <h4>Question</h4>
        <p>Where are orders geographically concentrated, and does that line up with where
        shipping cost could actually be optimized?</p>
        <p style="font-weight:600; color:{COLORS['primary_dark']};">
        Demand is concentrated in Java, mainly Jabodetabek, West Java, Banten and Central
        Java. Stocking inventory or setting up a dropship point near that cluster would cut
        the average shipping distance, and with it the shipping subsidy cost, for most orders.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top_n = st.slider("Show top N provinces", 5, len(region), 10)
view = region.sort_values("revenue_rp", ascending=False).head(top_n)

c1, c2 = st.columns(2)
with c1:
    st.markdown("##### Revenue by province")
    fig = go.Figure(go.Bar(
        x=view["revenue_rp"], y=view["Provinsi"], orientation="h",
        marker_color=CATEGORICAL_SEQUENCE[0],
    ))
    fig.update_layout(height=max(380, 28 * len(view)), xaxis_title="Revenue (Rp)", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("##### Order share by province")
    top8 = region.sort_values("orders", ascending=False).head(8).copy()
    others = region.sort_values("orders", ascending=False).iloc[8:]["orders"].sum()
    labels = list(top8["Provinsi"]) + (["Others"] if others > 0 else [])
    values = list(top8["orders"]) + ([others] if others > 0 else [])
    fig2 = go.Figure(go.Pie(labels=labels, values=values, hole=0.45, marker_colors=CATEGORICAL_SEQUENCE))
    fig2.update_layout(height=max(380, 28 * len(view)))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("##### Top 30 cities and districts by revenue")
fig3 = go.Figure(go.Bar(
    x=city["revenue_rp"], y=city["Kota/Kabupaten"] + " (" + city["Provinsi"] + ")",
    orientation="h", marker_color=CATEGORICAL_SEQUENCE[1],
))
fig3.update_layout(height=700, xaxis_title="Revenue (Rp)", yaxis=dict(autorange="reversed"))
st.plotly_chart(fig3, use_container_width=True)

with st.expander("View the full province table"):
    st.dataframe(
        region.rename(columns={"Provinsi": "Province", "orders": "Orders", "revenue_rp": "Revenue (Rp)"}),
        use_container_width=True, hide_index=True,
    )
