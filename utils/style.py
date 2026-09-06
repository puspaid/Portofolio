"""
Shared visual identity for the dashboard: color palette, CSS injection,
and a reusable Plotly template so every chart across every page looks
consistent with the reference design (deep burgundy / rose / cream).
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# ---------------------------------------------------------------------------
# Color palette (sampled from the provided reference dashboard image)
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#8C2A4B",       # deep burgundy, headlines and primary KPI values
    "primary_dark": "#5C1B33",  # darker burgundy, emphasis and negative deltas
    "accent": "#C9678A",        # rose, secondary series and highlights
    "accent_light": "#E8AFC3",  # light rose, tertiary series
    "accent_pale": "#F6DCE4",   # pale rose, chart fills and backgrounds
    "bg": "#FBF6F4",            # cream page background
    "card": "#FFFFFF",          # card background
    "border": "#F0E1E6",        # card border
    "text": "#3B2430",          # primary text
    "text_muted": "#8C7078",    # secondary text / captions
    "positive": "#2E7D5B",      # profit / good margin
    "negative": "#B23A48",      # loss / bad margin
    "warning": "#C9862E",       # caution / regulatory notes
}

CATEGORICAL_SEQUENCE = [
    COLORS["primary"], COLORS["accent"], COLORS["accent_light"],
    COLORS["primary_dark"], COLORS["warning"], COLORS["positive"],
    "#9E5B72", "#D9A0B3", "#733A4E", "#E0C4CE",
]

SCENARIO_COLORS = {
    "efisien": COLORS["positive"],
    "umum": COLORS["primary"],
    "ketat": COLORS["negative"],
}

SCENARIO_LABELS = {
    "efisien": "Efficient (COGS 35%)",
    "umum": "Typical (COGS 55%)",
    "ketat": "Tight (COGS 70%)",
}


def register_plotly_template():
    """Register a Plotly template matching the dashboard palette."""
    template = go.layout.Template()
    template.layout = go.Layout(
        font=dict(family="Segoe UI, Helvetica, Arial, sans-serif", color=COLORS["text"], size=13),
        colorway=CATEGORICAL_SEQUENCE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=17, color=COLORS["primary_dark"])),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], linecolor=COLORS["border"]),
        yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], linecolor=COLORS["border"]),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    pio.templates["marketplace_dashboard"] = template
    pio.templates.default = "marketplace_dashboard"


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {COLORS['bg']};
        }}
        h1, h2, h3 {{
            color: {COLORS['primary_dark']} !important;
            font-weight: 700 !important;
        }}
        p, li, span, label {{
            color: {COLORS['text']};
        }}
        [data-testid="stMetric"] {{
            background-color: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 16px 18px 10px 18px;
            box-shadow: 0 2px 10px rgba(140, 42, 75, 0.06);
        }}
        [data-testid="stMetricValue"] {{
            color: {COLORS['primary']};
            font-weight: 700;
        }}
        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_muted']};
        }}
        .biz-card {{
            background-color: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-left: 5px solid {COLORS['primary']};
            border-radius: 12px;
            padding: 20px 22px;
            margin-bottom: 16px;
            box-shadow: 0 2px 10px rgba(140, 42, 75, 0.06);
        }}
        .biz-card h4 {{
            color: {COLORS['primary_dark']};
            margin-top: 0;
        }}
        .verdict-label {{
            display: inline-block;
            background-color: {COLORS['accent_pale']};
            color: {COLORS['primary_dark']};
            font-weight: 700;
            padding: 6px 16px;
            border-radius: 6px;
            font-size: 0.9rem;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .section-divider {{
            border: none;
            border-top: 1px solid {COLORS['border']};
            margin: 28px 0 20px 0;
        }}
        [data-testid="stSidebar"] {{
            background-color: {COLORS['card']};
            border-right: 1px solid {COLORS['border']};
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {COLORS['text_muted']};
        }}
        .stTabs [aria-selected="true"] {{
            color: {COLORS['primary']} !important;
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_theme():
    register_plotly_template()
    inject_css()


def fmt_rp(value: float, decimals: int = 0) -> str:
    """Format a number as Indonesian Rupiah, e.g. Rp 1.045.550.734."""
    if value is None:
        return "-"
    sign = "-" if value < 0 else ""
    value = abs(value)
    s = f"{value:,.{decimals}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sign}Rp {s}"


def fmt_pct(value: float, decimals: int = 1) -> str:
    if value is None:
        return "-"
    return f"{value:,.{decimals}f}%"
