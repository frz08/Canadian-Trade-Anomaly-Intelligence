"""
CIMT Trade Anomaly Intelligence Dashboard
==========================================
Run:  streamlit run app.py
Deps: pip install -r requirements.txt
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CIMT Trade Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0E0E0E;
    color: #F5F5F5;
}
.stApp { background-color: #0E0E0E; }

[data-testid="stSidebar"] {
    background-color: #141414;
    border-right: 1px solid #2A2A2A;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    color: #8A8A8A !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

.anomaly-card {
    background: #1C1C1C;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 12px;
}
.anomaly-card-spike { border-left: 3px solid #5BC17A; }
.anomaly-card-drop  { border-left: 3px solid #E05555; }

.card-chapter    { font-size: 11px; color: #555; font-weight: 500; }
.card-value      { font-size: 24px; font-weight: 700; letter-spacing: -0.02em; margin: 4px 0; }
.card-value-up   { color: #5BC17A; }
.card-value-down { color: #E05555; }
.card-meta       { font-size: 12px; color: #555; font-family: monospace; }
.card-name       { font-size: 14px; color: #888; margin-top: 6px; font-weight: 500; line-height: 1.4; }

.pill {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    font-family: monospace;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.05em;
}
.pill-spike  { background: #0d2e1a; color: #5BC17A; border: 1px solid #1a4a2a; }
.pill-drop   { background: #2e0d0d; color: #E05555; border: 1px solid #4a1a1a; }

.ai-panel {
    background: #141414;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 20px 22px;
    margin-top: 16px;
}
.ai-panel-header {
    font-size: 11px;
    color: #4A90D9;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.ai-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4A90D9;
    display: inline-block;
    margin-right: 6px;
}
.ai-text { font-size: 13px; color: #C0C0C0; line-height: 1.75; }

.metric-card {
    background: #1C1C1C;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 18px 20px;
}
.metric-label { font-size: 11px; color: #555; font-weight: 500;
                letter-spacing: 0.06em; text-transform: uppercase; }
.metric-value { font-size: 28px; font-weight: 700; letter-spacing: -0.02em;
                color: #F5F5F5; margin: 6px 0 2px; }
.metric-sub   { font-size: 12px; color: #444; }

.section-header {
    font-size: 11px; font-weight: 600; color: #555;
    letter-spacing: 0.1em; text-transform: uppercase;
    border-bottom: 1px solid #2A2A2A;
    padding-bottom: 8px; margin: 24px 0 16px;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: #1C1C1C !important;
    border-color: #2A2A2A !important;
    color: #F5F5F5 !important;
}
.stButton > button {
    background: #1C1C1C; color: #4A90D9;
    border: 1px solid #1e3a5f; border-radius: 6px;
    font-size: 12px; font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.04em; padding: 6px 16px;
}
.stButton > button:hover {
    background: #1a2433; border-color: #4A90D9; color: #7ab8f5;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# GROQ SETUP
# =============================================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data
def load_data():
    try:
        anomalies    = pd.read_parquet("fact_anomalies")
        trade_series = pd.read_parquet("trade_series")
    except Exception:
        anomalies    = pd.read_csv("fact_anomalies.csv")
        trade_series = pd.read_csv("trade_series.csv")

    anomalies["Full_Date"]    = pd.to_datetime(anomalies["Full_Date"])
    trade_series["Full_Date"] = pd.to_datetime(trade_series["Full_Date"])
    anomalies["Pct_Display"]  = (anomalies["Pct_Change"] * 100).round(1)
    return anomalies, trade_series

anomalies, trade_series = load_data()

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("""
        <div style='padding: 20px 0 16px;'>
            <div style='font-size:16px;font-weight:700;color:#F5F5F5;'>CIMT Intelligence</div>
            <div style='font-size:11px;color:#444;margin-top:4px;'>Trade Anomaly Detection</div>
        </div>
        <hr style='border:none;border-top:1px solid #2A2A2A;margin:0 0 20px;'/>
    """, unsafe_allow_html=True)

    trade_type        = st.selectbox("Trade type", ["All", "Export", "Import"])
    anomaly_type      = st.selectbox("Anomaly type", ["All", "SPIKE", "DROP"])
    all_chapters      = sorted(anomalies["Chapter_Name"].dropna().unique().tolist())
    selected_chapters = st.multiselect("HS Chapters", options=all_chapters,
                                       default=[], placeholder="All chapters")
    min_year   = int(anomalies["Year_Num"].min())
    max_year   = int(anomalies["Year_Num"].max())
    year_range = st.slider("Year range", min_value=min_year, max_value=max_year,
                           value=(min_year, max_year))
    z_threshold = st.slider("Min z-score", min_value=1.0, max_value=5.0,
                            value=2.0, step=0.1)
    st.markdown("""
        <hr style='border:none;border-top:1px solid #2A2A2A;margin:20px 0;'/>
        <div style='font-size:11px;color:#333;'>Data: Statistics Canada CIMT<br/>1990 – 2026 · 157M rows</div>
    """, unsafe_allow_html=True)

# =============================================================================
# FILTER
# =============================================================================

filtered = anomalies.copy()
if trade_type != "All":
    filtered = filtered[filtered["Trade_Type"] == trade_type]
if anomaly_type != "All":
    filtered = filtered[filtered["Anomaly_Type"] == anomaly_type]
if selected_chapters:
    filtered = filtered[filtered["Chapter_Name"].isin(selected_chapters)]
filtered = filtered[
    (filtered["Year_Num"] >= year_range[0]) &
    (filtered["Year_Num"] <= year_range[1])
]
filtered = filtered[filtered["Z_Score"].abs() >= z_threshold]
filtered = filtered.sort_values("Full_Date", ascending=False)

# =============================================================================
# HEADER
# =============================================================================

st.markdown("""
    <div style='padding: 28px 0 8px;'>
        <div style='font-size:26px;font-weight:700;color:#F5F5F5;letter-spacing:-0.02em;'>
            Canadian Trade Anomaly Intelligence
        </div>
        <div style='font-size:13px;color:#555;margin-top:6px;'>
            Automated spike and drop detection across HS chapters · 1990–2026
        </div>
    </div>
""", unsafe_allow_html=True)

# =============================================================================
# METRICS
# =============================================================================

total_anomalies = len(filtered)
total_spikes    = len(filtered[filtered["Anomaly_Type"] == "SPIKE"])
total_drops     = len(filtered[filtered["Anomaly_Type"] == "DROP"])
max_z           = filtered["Z_Score"].abs().max() if len(filtered) > 0 else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Total anomalies</div>"
                f"<div class='metric-value'>{total_anomalies:,}</div>"
                f"<div class='metric-sub'>across all chapters</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Spikes</div>"
                f"<div class='metric-value' style='color:#5BC17A'>{total_spikes:,}</div>"
                f"<div class='metric-sub'>above baseline</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Drops</div>"
                f"<div class='metric-value' style='color:#E05555'>{total_drops:,}</div>"
                f"<div class='metric-sub'>below baseline</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Strongest signal</div>"
                f"<div class='metric-value'>{abs(max_z):.1f}"
                f"<span style='font-size:14px;color:#555;font-weight:400'>σ</span></div>"
                f"<div class='metric-sub'>max z-score</div></div>", unsafe_allow_html=True)

# =============================================================================
# CHART — full width
# =============================================================================

st.markdown("<div class='section-header'>Anomaly timeline</div>", unsafe_allow_html=True)

if len(filtered) == 0:
    st.markdown("<div style='background:#1C1C1C;border:1px solid #2A2A2A;border-radius:10px;"
                "padding:40px;text-align:center;color:#444;font-size:13px;'>"
                "No anomalies match the current filters.</div>", unsafe_allow_html=True)
else:
    chart_chapter = selected_chapters[0] if selected_chapters else filtered["Chapter_Name"].iloc[0]
    bg = trade_series[
        (trade_series["Chapter_Name"] == chart_chapter) &
        (trade_series["Trade_Type"] == (trade_type if trade_type != "All" else "Export"))
    ].sort_values("Full_Date")

    spikes = filtered[filtered["Anomaly_Type"] == "SPIKE"]
    drops  = filtered[filtered["Anomaly_Type"] == "DROP"]
    fig    = go.Figure()

    if len(bg) > 0:
        fig.add_trace(go.Scatter(x=bg["Full_Date"], y=bg["Total_Value"], mode="lines",
            name=chart_chapter, line=dict(color="#2A2A2A", width=1.5),
            hovertemplate="%{x|%b %Y}<br>$%{y:,.0f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=bg["Full_Date"], y=bg["Baseline_Mean"], mode="lines",
            name="12-month baseline", line=dict(color="#333333", width=1, dash="dot"),
            hovertemplate="Baseline: $%{y:,.0f}<extra></extra>"))

    if len(spikes) > 0:
        fig.add_trace(go.Scatter(x=spikes["Full_Date"], y=spikes["Total_Value"],
            mode="markers", name="Spike",
            marker=dict(color="#5BC17A", size=9, line=dict(color="#0d2e1a", width=1.5)),
            hovertemplate="<b>SPIKE</b><br>%{x|%b %Y}<br>%{customdata[0]}<br>"
                          "z=%{customdata[1]:.2f} · +%{customdata[2]:.1f}%<extra></extra>",
            customdata=spikes[["Chapter_Name", "Z_Score", "Pct_Display"]].values))

    if len(drops) > 0:
        fig.add_trace(go.Scatter(x=drops["Full_Date"], y=drops["Total_Value"],
            mode="markers", name="Drop",
            marker=dict(color="#E05555", size=9, line=dict(color="#4a1a1a", width=1.5)),
            hovertemplate="<b>DROP</b><br>%{x|%b %Y}<br>%{customdata[0]}<br>"
                          "z=%{customdata[1]:.2f} · %{customdata[2]:.1f}%<extra></extra>",
            customdata=drops[["Chapter_Name", "Z_Score", "Pct_Display"]].values))

    fig.update_layout(
        paper_bgcolor="#0E0E0E", plot_bgcolor="#141414",
        font=dict(family="Inter, sans-serif", color="#8A8A8A", size=11),
        margin=dict(l=60, r=20, t=16, b=40), height=420,
        legend=dict(
            bgcolor="#1C1C1C", bordercolor="#2A2A2A", borderwidth=1,
            font=dict(size=11, color="#8A8A8A"),
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0
        ),
        xaxis=dict(
            gridcolor="#1C1C1C", linecolor="#2A2A2A", zeroline=False,
            tickformat="%Y", dtick="M24", tickangle=-45
        ),
        yaxis=dict(
            gridcolor="#1C1C1C", linecolor="#2A2A2A", zeroline=False,
            tickformat="$,.2s"
        ),
        hovermode="closest"
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if len(bg) == 0:
        st.markdown(
            f"<div style='font-size:11px;color:#555;margin-top:4px;'>"
            f"No trade series data for <b style='color:#888'>{chart_chapter}</b> — "
            f"select a chapter in the sidebar to see the background line.</div>",
            unsafe_allow_html=True
        )

# =============================================================================
# ANOMALY CARDS — top 3 horizontal row below chart
# =============================================================================

st.markdown("<div class='section-header'>Top anomalies</div>", unsafe_allow_html=True)

if len(filtered) == 0:
    st.markdown("<div style='color:#444;font-size:13px;'>No anomalies match filters.</div>",
                unsafe_allow_html=True)
else:
    def render_card(row):
        is_spike  = row["Anomaly_Type"] == "SPIKE"
        pill_cls  = "pill-spike" if is_spike else "pill-drop"
        card_cls  = "anomaly-card-spike" if is_spike else "anomaly-card-drop"
        val_cls   = "card-value-up" if is_spike else "card-value-down"
        sign      = "+" if is_spike else ""
        month_str = pd.Timestamp(row["Full_Date"]).strftime("%b %Y")
        st.markdown(f"""
            <div class='anomaly-card {card_cls}'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span class='card-chapter'>Chapter {row['Chapter_Code']}</span>
                    <span class='pill {pill_cls}'>{row['Anomaly_Type']}</span>
                </div>
                <div class='card-value {val_cls}'>{sign}{row['Pct_Display']}%</div>
                <div class='card-meta'>z = {row['Z_Score']:+.2f} · {row['Trade_Type']} · {month_str}</div>
                <div class='card-name'>{row['Chapter_Name']}</div>
            </div>
        """, unsafe_allow_html=True)

    top3 = filtered.head(3)
    col1, col2, col3 = st.columns(3, gap="medium")
    for i, (_, row) in enumerate(top3.iterrows()):
        with [col1, col2, col3][i]:
            render_card(row)

# =============================================================================
# AI EXPLANATION — Groq
# =============================================================================

st.markdown("<div class='section-header'>AI research — explain an anomaly</div>",
            unsafe_allow_html=True)

if len(filtered) == 0:
    st.markdown("<div style='color:#444;font-size:13px;'>Apply filters to surface anomalies.</div>",
                unsafe_allow_html=True)
else:
    filtered["_label"] = (
        filtered["Anomaly_Type"] + " · Ch." + filtered["Chapter_Code"].astype(str)
        + " · " + filtered["Full_Date"].dt.strftime("%b %Y")
        + " · " + filtered["Chapter_Name"].str[:30]
        + "  (z=" + filtered["Z_Score"].apply(lambda x: f"{x:+.2f}") + ")"
    )

    selected_label = st.selectbox("Select anomaly to research",
                                  options=filtered["_label"].tolist(),
                                  label_visibility="collapsed")
    selected_row = filtered[filtered["_label"] == selected_label].iloc[0]

    col_info, col_btn = st.columns([3, 1])

    with col_info:
        month_str = pd.Timestamp(selected_row["Full_Date"]).strftime("%B %Y")
        is_spike  = selected_row["Anomaly_Type"] == "SPIKE"
        direction = "spiked" if is_spike else "dropped"
        color     = "#5BC17A" if is_spike else "#E05555"
        sign      = "+" if is_spike else ""
        st.markdown(f"""
            <div style='background:#1C1C1C;border:1px solid #2A2A2A;border-radius:8px;
                        padding:14px 16px;font-size:13px;color:#8A8A8A;line-height:1.7;'>
                Canadian <b style='color:#F5F5F5'>{selected_row['Trade_Type'].lower()}s</b>
                of <b style='color:#F5F5F5'>Chapter {selected_row['Chapter_Code']}
                ({selected_row['Chapter_Name']})</b>
                {direction} <b style='color:{color}'>{sign}{selected_row['Pct_Display']}%</b>
                in <b style='color:#F5F5F5'>{month_str}</b>
                (z-score {selected_row['Z_Score']:+.2f}).
            </div>
        """, unsafe_allow_html=True)

    with col_btn:
        explain_clicked = st.button("Why did this happen?", use_container_width=True)

    if explain_clicked:
        if not GROQ_API_KEY:
            st.markdown("<div class='ai-panel' style='color:#E05555;font-size:13px;'>"
                        "GROQ_API_KEY not found. Add it to your .env file.</div>",
                        unsafe_allow_html=True)
        else:
            month_str  = pd.Timestamp(selected_row["Full_Date"]).strftime("%B %Y")
            direction  = "spike" if selected_row["Anomaly_Type"] == "SPIKE" else "drop"
            trade_word = selected_row["Trade_Type"].lower() + "s"

            prompt = (
                f"Canadian merchandise trade data shows a significant {direction} in "
                f"{trade_word} of HS Chapter {selected_row['Chapter_Code']} "
                f"({selected_row['Chapter_Name']}) in {month_str}. "
                f"The value was {selected_row['Pct_Display']:+.1f}% from the 12-month baseline "
                f"with a z-score of {selected_row['Z_Score']:+.2f}. "
                f"Explain in 3-4 sentences what real-world events, policies, or market "
                f"conditions most likely caused this {direction}. Be specific — name actual "
                f"events, trade agreements, or disruptions where possible. "
                f"End with a brief list of likely sources."
            )

            st.markdown(f"""
                <div class='ai-panel'>
                    <div class='ai-panel-header'>
                        <span class='ai-dot'></span>
                        AI Research · Ch.{selected_row['Chapter_Code']} · {month_str}
                    </div>
            """, unsafe_allow_html=True)

            response_placeholder = st.empty()
            full_response = ""

            try:
                client = Groq(api_key=GROQ_API_KEY)
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_response += delta
                        response_placeholder.markdown(
                            f"<div class='ai-text'>{full_response}</div>",
                            unsafe_allow_html=True
                        )
            except Exception as e:
                st.markdown(f"<div style='color:#E05555;font-size:13px;'>Error: {str(e)}</div>",
                            unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
