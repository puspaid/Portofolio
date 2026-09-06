import streamlit as st
import plotly.graph_objects as go

from utils.style import apply_theme, COLORS, fmt_rp, fmt_pct
from utils.data_loader import load_category_breakdown

st.set_page_config(page_title="Category Breakdown", layout="wide")
apply_theme()

st.title("Category Breakdown")
st.caption("Revenue, order volume and margin across 37 product categories.")

cat = load_category_breakdown().copy()

scenario_label = st.selectbox(
    "Cost-of-goods scenario for margin highlighting",
    ["umum", "efisien", "ketat"],
    format_func=lambda x: {"umum": "Typical (55%)", "efisien": "Efficient (35%)", "ketat": "Tight (70%)"}[x],
)
margin_col = f"margin_{scenario_label}_pct"
profit_col = f"profit_{scenario_label}_rp"

st.markdown(
    f"""
    <div class="biz-card">
        <h4>Question</h4>
        <p>Are the best-selling categories actually the most profitable ones?</p>
        <p style="font-weight:600; color:{COLORS['primary_dark']};">
        No. The highest-volume categories, Celengan, Mangkok Sambal/Saus and Aksesoris
        Pintu, carry thin or negative margins once realistic cost of goods is applied.
        Smaller categories such as Seal/Baut/Roof and Nampan/Tray are the ones actually
        making money. Pushing the current best-sellers harder would grow losses, not profit.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top_n = st.slider("Show top N categories by revenue", 5, 37, 15)
view = cat.sort_values("revenue_rp", ascending=False).head(top_n)

st.markdown(f"##### Revenue by category, colored by margin ({scenario_label} scenario)")
colors = [COLORS["negative"] if m < 0 else (COLORS["warning"] if m < 5 else COLORS["positive"]) for m in view[margin_col]]
fig = go.Figure(go.Bar(
    x=view["revenue_rp"], y=view["Kategori_Utama"], orientation="h",
    marker_color=colors,
    text=[f"{fmt_pct(m)}" for m in view[margin_col]],
    textposition="outside",
))
fig.update_layout(height=max(400, 26 * len(view)), xaxis_title="Revenue (Rp)", yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, use_container_width=True)
st.caption("Green means a healthy margin of 5% or more. Amber is thin, between 0 and 5%. Red is a loss.")

c1, c2 = st.columns(2)
with c1:
    st.markdown("##### Five most profitable categories")
    best = cat.sort_values(profit_col, ascending=False).head(5)
    st.dataframe(
        best[["Kategori_Utama", "orders", "revenue_rp", profit_col, margin_col]].rename(columns={
            "Kategori_Utama": "Category", "orders": "Orders", "revenue_rp": "Revenue (Rp)",
            profit_col: "Net profit (Rp)", margin_col: "Margin (%)",
        }),
        hide_index=True, use_container_width=True,
    )
with c2:
    st.markdown("##### Five biggest losses")
    worst = cat.sort_values(profit_col, ascending=True).head(5)
    st.dataframe(
        worst[["Kategori_Utama", "orders", "revenue_rp", profit_col, margin_col]].rename(columns={
            "Kategori_Utama": "Category", "orders": "Orders", "revenue_rp": "Revenue (Rp)",
            profit_col: "Net profit (Rp)", margin_col: "Margin (%)",
        }),
        hide_index=True, use_container_width=True,
    )

with st.expander("View the full category table, all 37 categories"):
    st.dataframe(
        cat.rename(columns={"Kategori_Utama": "Category", "orders": "Orders", "revenue_rp": "Revenue (Rp)"}),
        use_container_width=True, hide_index=True,
    )
