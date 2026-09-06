import streamlit as st
import plotly.graph_objects as go

from utils.style import apply_theme, COLORS, fmt_rp, fmt_pct
from utils.data_loader import load_monthly_trend

st.set_page_config(page_title="Monthly Trends", layout="wide")
apply_theme()

st.title("Monthly Trends")
st.caption("Revenue, net profit under three cost-of-goods scenarios, and average order value over time.")

monthly = load_monthly_trend()

min_d, max_d = monthly["Periode"].min(), monthly["Periode"].max()
date_range = st.slider(
    "Period range",
    min_value=min_d.to_pydatetime(),
    max_value=max_d.to_pydatetime(),
    value=(min_d.to_pydatetime(), max_d.to_pydatetime()),
    format="MMM YYYY",
)
mask = (monthly["Periode"] >= date_range[0]) & (monthly["Periode"] <= date_range[1])
view = monthly[mask]

st.markdown(
    f"""
    <div class="biz-card">
        <h4>Question</h4>
        <p>Is month-to-month performance improving, and is that something more orders can
        fix, or is it a margin problem?</p>
        <p style="font-weight:600; color:{COLORS['primary_dark']};">
        Order volume is trending up over this window, but revenue, average order value and
        net profit are trending down at the same time. More orders aren't making up for the
        drop in value per order.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Orders in range", f"{int(view['orders'].sum()):,}".replace(",", "."))
c2.metric("Revenue in range", fmt_rp(view["revenue_rp"].sum()))
c3.metric("Average AOV in range", fmt_rp(view["aov_rp"].mean()))
c4.metric("Net profit, typical scenario", fmt_rp(view["profit_umum_rp"].sum()))

st.markdown("##### Revenue and net profit across three scenarios")
fig = go.Figure()
fig.add_trace(go.Scatter(x=view["Periode"], y=view["revenue_rp"], name="Revenue",
                          fill="tozeroy", line=dict(color=COLORS["accent_light"], width=2),
                          fillcolor="rgba(232,175,195,0.30)"))
fig.add_trace(go.Scatter(x=view["Periode"], y=view["profit_efisien_rp"], name="Profit, efficient (35%)",
                          line=dict(color=COLORS["positive"], width=2, dash="dot")))
fig.add_trace(go.Scatter(x=view["Periode"], y=view["profit_umum_rp"], name="Profit, typical (55%)",
                          line=dict(color=COLORS["primary"], width=3)))
fig.add_trace(go.Scatter(x=view["Periode"], y=view["profit_ketat_rp"], name="Profit, tight (70%)",
                          line=dict(color=COLORS["negative"], width=2, dash="dot")))
fig.add_hline(y=0, line_color=COLORS["text_muted"], line_width=1)
fig.update_layout(height=420, hovermode="x unified", yaxis_title="IDR",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

st.markdown("##### Average order value")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=view["Periode"], y=view["aov_rp"], name="AOV",
                           line=dict(color=COLORS["primary_dark"], width=3), mode="lines+markers"))
fig2.update_layout(height=320, yaxis_title="IDR per order")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("##### Orders per month")
fig3 = go.Figure(go.Bar(x=view["Periode"], y=view["orders"], marker_color=COLORS["accent"]))
fig3.update_layout(height=300, yaxis_title="Orders")
st.plotly_chart(fig3, use_container_width=True)

with st.expander("View underlying monthly data"):
    st.dataframe(
        view.rename(columns={
            "Periode": "Period", "orders": "Orders", "revenue_rp": "Revenue (Rp)",
            "profit_efisien_rp": "Profit efficient (Rp)", "profit_umum_rp": "Profit typical (Rp)",
            "profit_ketat_rp": "Profit tight (Rp)", "aov_rp": "AOV (Rp)",
        }),
        use_container_width=True, hide_index=True,
    )
