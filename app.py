import streamlit as st
import pandas as pd
import os
from src.agent.graph import build_graph

# =============== PAGE CONFIG =================
st.set_page_config(
    page_title="EV Planner Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============== REDESIGNED CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
    --obsidian:     #080b0f;
    --obsidian-2:   #0d1117;
    --obsidian-3:   #111720;
    --obsidian-4:   #161e2a;
    --amber:        #f59e0b;
    --amber-dim:    #d97706;
    --amber-glow:   rgba(245, 158, 11, 0.12);
    --amber-trace:  rgba(245, 158, 11, 0.06);
    --teal:         #2dd4bf;
    --teal-dim:     #14b8a6;
    --teal-glow:    rgba(45, 212, 191, 0.10);
    --teal-trace:   rgba(45, 212, 191, 0.05);
    --slate:        #94a3b8;
    --slate-dim:    #64748b;
    --wire:         rgba(255,255,255,0.055);
    --wire-hover:   rgba(255,255,255,0.09);
    --text-hi:      #f0ece4;
    --text-mid:     #8b9aa8;
    --text-lo:      #4a5568;
    --font-display: 'Syne', sans-serif;
    --font-body:    'Instrument Sans', sans-serif;
    --font-mono:    'DM Mono', monospace;
    --r-sm:  6px;
    --r-md:  12px;
    --r-lg:  18px;
    --r-xl:  24px;
}

html, body, [class*="css"], .stApp {
    font-family: var(--font-body) !important;
    background: var(--obsidian) !important;
    color: var(--text-hi) !important;
}

/* ─── NOISE GRAIN OVERLAY ─── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* ─── AMBIENT GLOW ─── */
.stApp::after {
    content: '';
    position: fixed;
    top: -30vh;
    left: 50%;
    transform: translateX(-50%);
    width: 70vw;
    height: 60vh;
    background: radial-gradient(ellipse at center,
        rgba(245,158,11,0.035) 0%,
        rgba(45,212,191,0.025) 40%,
        transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.stApp > .main { position: relative; z-index: 1; }

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--amber-dim);
    border-radius: 99px;
    opacity: 0.4;
}

/* ─── MAIN HEADER ─── */
.ev-header-wrap {
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid var(--wire);
    margin-bottom: 2rem;
    position: relative;
}

.ev-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 300;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.ev-eyebrow::before {
    content: '';
    display: inline-block;
    width: 24px;
    height: 1px;
    background: var(--amber);
    opacity: 0.6;
}

.ev-title {
    font-family: var(--font-display) !important;
    font-size: 3.8rem !important;
    font-weight: 800 !important;
    line-height: 0.95 !important;
    letter-spacing: -0.04em !important;
    color: var(--text-hi) !important;
    margin: 0 0 0.6rem !important;
}

.ev-title em {
    font-style: normal;
    -webkit-text-stroke: 1px var(--amber);
    color: transparent;
}

.ev-sub {
    font-family: var(--font-body);
    font-size: 0.9rem;
    color: var(--text-mid);
    font-weight: 400;
    letter-spacing: 0.01em;
}

.ev-sub strong {
    color: var(--teal);
    font-weight: 500;
}

.ev-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 14px;
    background: rgba(45,212,191,0.07);
    border: 1px solid rgba(45,212,191,0.18);
    border-radius: 99px;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--teal);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 400;
    float: right;
    margin-top: 8px;
}

.ev-status-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--teal);
    animation: pulse-teal 2.5s ease-in-out infinite;
}

@keyframes pulse-teal {
    0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(45,212,191,0.4); }
    50%      { opacity:0.6; box-shadow: 0 0 0 5px rgba(45,212,191,0); }
}

/* ─── SIDEBAR ─── */
section[data-testid="stSidebar"] {
    background: var(--obsidian-2) !important;
    border-right: 1px solid var(--wire) !important;
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.25rem !important;
}

.sb-logo {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-hi);
    margin-bottom: 2px;
}

.sb-logo span {
    color: var(--amber);
}

.sb-tagline {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-lo);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 300;
    margin-bottom: 1.8rem;
}

.sb-section {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 400;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-lo);
    margin: 1.4rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sb-section::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--wire);
}

div[data-testid="stSidebar"] label {
    font-family: var(--font-body) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--text-mid) !important;
    letter-spacing: 0.01em !important;
}

div[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: var(--obsidian-3) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s;
}

div[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
    border-color: rgba(245,158,11,0.35) !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.06) !important;
}

div[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--obsidian-3) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
}

div[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
    color: var(--text-hi) !important;
}

/* session stat mini cards */
.sb-stat-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 0.6rem 0 1.2rem;
}

.sb-stat {
    background: var(--obsidian-3);
    border: 1px solid var(--wire);
    border-radius: var(--r-md);
    padding: 12px 10px;
    text-align: center;
}

.sb-stat-val {
    font-family: var(--font-mono);
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--amber);
    line-height: 1;
    margin-bottom: 4px;
}

.sb-stat-label {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    color: var(--text-lo);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.sb-tip {
    background: var(--obsidian-3);
    border: 1px solid var(--wire);
    border-left: 2px solid var(--amber-dim);
    border-radius: 0 var(--r-md) var(--r-md) 0;
    padding: 14px 14px;
    margin-top: 1.2rem;
}

.sb-tip-head {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--amber);
    margin-bottom: 6px;
    font-weight: 500;
}

.sb-tip-body {
    font-size: 0.76rem;
    color: var(--text-mid);
    line-height: 1.6;
}

.sb-tip-body em {
    font-style: normal;
    color: var(--teal);
}

.sb-version {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--wire);
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-lo);
    text-align: center;
    letter-spacing: 0.06em;
    opacity: 0.5;
}

/* ─── BUTTONS ─── */
.stButton > button {
    font-family: var(--font-body) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    background: var(--obsidian-3) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
    color: var(--text-mid) !important;
    padding: 10px 16px !important;
    transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    background: var(--obsidian-4) !important;
    border-color: rgba(245,158,11,0.25) !important;
    color: var(--text-hi) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ─── QUICK ACTION CHIPS ─── */
.chip-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 0 0 2rem;
}

/* Override streamlit button inside chip context */
div[data-testid="column"] .stButton > button {
    background: var(--obsidian-3) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-lg) !important;
    color: var(--text-mid) !important;
    font-size: 0.8rem !important;
    padding: 12px 14px !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

div[data-testid="column"] .stButton > button:hover {
    background: var(--amber-trace) !important;
    border-color: rgba(245,158,11,0.22) !important;
    color: var(--text-hi) !important;
}

/* ─── CHAT MESSAGES ─── */
.stChatMessage {
    background: var(--obsidian-2) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-lg) !important;
    padding: 18px 20px !important;
    margin-bottom: 12px !important;
    transition: border-color 0.2s !important;
}

.stChatMessage[data-testid="stChatMessageAssistant"] {
    border-left: 2px solid var(--amber-dim) !important;
    border-radius: 0 var(--r-lg) var(--r-lg) 0 !important;
}

.stChatMessage[data-testid="stChatMessageUser"] {
    border-left: 2px solid var(--teal-dim) !important;
    border-radius: 0 var(--r-lg) var(--r-lg) 0 !important;
    background: var(--obsidian-3) !important;
}

.stChatMessage p {
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
    line-height: 1.75 !important;
    color: var(--text-hi) !important;
}

.stChatMessage strong { color: var(--amber) !important; font-weight: 600 !important; }

.stChatMessage code {
    font-family: var(--font-mono) !important;
    background: rgba(245,158,11,0.07) !important;
    border: 1px solid rgba(245,158,11,0.12) !important;
    border-radius: var(--r-sm) !important;
    padding: 1px 6px !important;
    font-size: 0.8rem !important;
    color: var(--amber) !important;
    font-weight: 300 !important;
}

.stChatMessage pre {
    background: var(--obsidian) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
}

.stChatMessage pre code {
    background: transparent !important;
    border: none !important;
    color: var(--teal) !important;
}

/* ─── CHAT INPUT ─── */
.stChatInputContainer textarea {
    background: var(--obsidian-2) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-lg) !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body) !important;
    font-size: 0.88rem !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

.stChatInputContainer textarea:focus {
    border-color: rgba(245,158,11,0.3) !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.06) !important;
}

.stChatInputContainer textarea::placeholder {
    color: var(--text-lo) !important;
    font-style: italic;
}

/* ─── METRIC CARDS ─── */
div[data-testid="stMetric"] {
    background: var(--obsidian-2) !important;
    border: 1px solid var(--wire) !important;
    border-top: 2px solid var(--amber-dim) !important;
    border-radius: 0 0 var(--r-md) var(--r-md) !important;
    padding: 20px 18px !important;
    transition: border-color 0.2s, transform 0.2s !important;
    position: relative;
}

div[data-testid="stMetric"]:hover {
    border-color: rgba(245,158,11,0.3) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    font-weight: 300 !important;
    color: var(--text-lo) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

div[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text-hi) !important;
    letter-spacing: -0.02em !important;
}

/* ─── CHARTS ─── */
.stArrowContainer > div,
.element-container .stChart {
    background: var(--obsidian-2) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-lg) !important;
    padding: 16px !important;
}

/* ─── EXPANDER ─── */
.streamlit-expanderHeader {
    background: var(--obsidian-2) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--text-mid) !important;
    padding: 12px 16px !important;
    transition: all 0.2s !important;
}

.streamlit-expanderHeader:hover {
    border-color: rgba(245,158,11,0.2) !important;
    color: var(--text-hi) !important;
}

.streamlit-expanderContent {
    background: var(--obsidian) !important;
    border: 1px solid var(--wire) !important;
    border-radius: 0 0 var(--r-md) var(--r-md) !important;
}

/* ─── SELECTBOX DROPDOWN ─── */
div[data-baseweb="popover"] {
    background: var(--obsidian-3) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
}

div[data-baseweb="popover"] li {
    color: var(--text-hi) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    transition: background 0.15s !important;
}

div[data-baseweb="popover"] li:hover {
    background: var(--amber-trace) !important;
}

/* ─── DIVIDER ─── */
hr {
    border: none !important;
    height: 1px !important;
    background: var(--wire) !important;
    margin: 2rem 0 !important;
}

/* ─── DASHBOARD ELEMENTS ─── */
.dash-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 10px;
}

.dash-title {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-hi);
    display: flex;
    align-items: center;
    gap: 10px;
}

.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--teal);
    box-shadow: 0 0 8px var(--teal);
    animation: pulse-teal 2s infinite;
}

.location-tag {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--amber);
    letter-spacing: 0.06em;
    font-weight: 400;
}

.load-badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 12px;
    border-radius: 99px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.load-high   { background: rgba(239,68,68,0.08);   border: 1px solid rgba(239,68,68,0.2);   color: #f87171; }
.load-medium { background: rgba(245,158,11,0.08);  border: 1px solid rgba(245,158,11,0.22); color: var(--amber); }
.load-low    { background: rgba(45,212,191,0.08);  border: 1px solid rgba(45,212,191,0.2);  color: var(--teal); }

.chart-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-lo);
    margin-bottom: 8px;
    font-weight: 300;
}

/* ─── EMPTY STATE ─── */
.empty-state {
    margin: 5rem auto;
    text-align: center;
    max-width: 380px;
}

.empty-icon {
    font-family: var(--font-mono);
    font-size: 2.5rem;
    color: var(--text-lo);
    opacity: 0.25;
    margin-bottom: 1.2rem;
    letter-spacing: -0.05em;
}

.empty-text {
    font-size: 0.88rem;
    color: var(--text-mid);
    line-height: 1.7;
}

.empty-text em {
    font-style: normal;
    color: var(--amber);
    font-weight: 500;
}

/* ─── JSON VIEWER ─── */
.stJson {
    background: var(--obsidian) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    font-weight: 300 !important;
}

/* ─── SPINNER ─── */
.stSpinner > div {
    border-color: rgba(245,158,11,0.12) !important;
    border-top-color: var(--amber) !important;
}

/* ─── ALERTS ─── */
.stAlert {
    border-radius: var(--r-md) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
}

/* ─── HIDE DEFAULTS ─── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "latest_report" not in st.session_state:
    st.session_state.latest_report = None
if "last_suggestion" not in st.session_state:
    st.session_state.last_suggestion = None
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">EV<span>⚡</span>Planner</div>
    <div class="sb-tagline">Infrastructure Intelligence</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Configuration</div>', unsafe_allow_html=True)

    location = st.text_input("Location", value="Mumbai", placeholder="e.g. Mumbai, Delhi...")
    region   = st.selectbox("Region Type", ["Urban", "Suburban", "Highway"])

    st.markdown('<div class="sb-section">Session</div>', unsafe_allow_html=True)

    msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    has_report = "✓" if st.session_state.latest_report else "—"

    st.markdown(f"""
    <div class="sb-stat-row">
        <div class="sb-stat">
            <div class="sb-stat-val">{msg_count}</div>
            <div class="sb-stat-label">Queries</div>
        </div>
        <div class="sb-stat">
            <div class="sb-stat-val" style="color:var(--teal);">{has_report}</div>
            <div class="sb-stat-label">Report</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Clear Session", use_container_width=True, key="clear_btn"):
        st.session_state.messages = []
        st.session_state.latest_report = None
        st.session_state.last_suggestion = None
        st.session_state.chat_started = False
        st.rerun()

    st.markdown("""
    <div class="sb-tip">
        <div class="sb-tip-head">Pro Tip</div>
        <div class="sb-tip-body">
            Ask follow-ups about <em>infrastructure costs</em>, 
            charger types, or <em>grid stability</em> for deeper analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-version">v2.0.0 — AI Powered</div>', unsafe_allow_html=True)


# ================= MAIN CONTENT =================
api_key_exists = os.getenv("GROQ_API_KEY") or ("GROQ_API_KEY" in st.secrets)

st.markdown("""
<div class="ev-header-wrap">
    <div class="ev-eyebrow">AI Infrastructure Agent</div>
    <div class="ev-title">EV <em>Charging</em><br>Planner Pro</div>
    <div class="ev-sub">Intelligent simulation &amp; <strong>strategic planning</strong> engine</div>
    <div class="ev-status-pill">
        <span class="ev-status-dot"></span>
        Agent Online
    </div>
</div>
""", unsafe_allow_html=True)

if not api_key_exists:
    st.markdown("""
    <div style="margin-top:2rem; padding:22px; background:rgba(239,68,68,0.05); border:1px solid rgba(239,68,68,0.14); border-left:2px solid #ef4444; border-radius:0 12px 12px 0;">
        <div style="font-family:var(--font-mono); font-size:0.68rem; text-transform:uppercase; letter-spacing:0.1em; color:#f87171; margin-bottom:8px; font-weight:400;">API Key Missing</div>
        <div style="font-size:0.84rem; color:var(--text-mid); line-height:1.6;">
            Set <code style="font-family:var(--font-mono); background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.15); border-radius:4px; padding:1px 6px; font-size:0.75rem; color:#f87171;">GROQ_API_KEY</code>
            in Settings → Secrets to activate the AI agent.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─── QUICK ACTIONS ───
suggestions = [
    {"icon": "⚡", "text": "Peak demand hour analysis"},
    {"icon": "🔌", "text": "Charger capacity requirements"},
    {"icon": "📊", "text": "Full demand pattern breakdown"},
    {"icon": "🏗️", "text": "Long-term infrastructure roadmap"},
]

st.markdown("""
<div style="font-family:var(--font-mono); font-size:0.62rem; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-lo); margin-bottom:10px; font-weight:300;">
    Quick Actions
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
chip_callbacks = {}

for idx, sug in enumerate(suggestions):
    col = col1 if idx % 2 == 0 else col2
    with col:
        clicked = st.button(f"{sug['icon']}  {sug['text']}", key=f"chip_{idx}", use_container_width=True)
        chip_callbacks[idx] = clicked

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─── CHAT HISTORY ───
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ─── AGENT ───
def run_agent(query):
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.chat_started = True

    with st.spinner("Analyzing infrastructure parameters..."):
        graph = build_graph()
        state = {
            "location": location,
            "region": region,
            "query": query,
            "history": st.session_state.messages[:-1]
        }
        result = graph.invoke(state)
        report   = result["final_report"]
        response = report["response"]
        st.session_state.latest_report = report

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


for idx, clicked in chip_callbacks.items():
    if clicked:
        query = suggestions[idx]["text"]
        if st.session_state.last_suggestion != query:
            st.session_state.last_suggestion = query
            run_agent(query)
            st.rerun()

if prompt := st.chat_input("Ask anything about EV infrastructure..."):
    run_agent(prompt)


# ─── DASHBOARD ───
if st.session_state.latest_report:
    report  = st.session_state.latest_report
    summary = report["demand_summary"]

    load_level = report.get("load_level", "Medium").lower()
    load_class = "load-high" if "high" in load_level else ("load-low" if "low" in load_level else "load-medium")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="dash-header">
        <div class="dash-title">
            <span class="live-dot"></span>
            Live Dashboard
            <span class="location-tag">/ {report['location']}</span>
        </div>
        <span class="load-badge {load_class}">{report['load_level']} Load</span>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Total Demand", f"{summary['total_daily_demand']} kWh")
    with m2:
        st.metric("Peak Hour", f"{summary['peak_hour']}:00")
    with m3:
        st.metric("Chargers Needed", summary["chargers_needed"])
    with m4:
        peak = max(summary.get("hourly_profile", [0])) if "hourly_profile" in summary else 0
        st.metric("Peak Demand", f"{peak} kW")

    if "hourly_profile" in summary:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="chart-label">24-Hour Demand Profile</div>', unsafe_allow_html=True)

        df_chart = pd.DataFrame({
            "Hour": [f"{h:02d}:00" for h in range(24)],
            "Demand (kWh)": summary["hourly_profile"]
        })
        st.bar_chart(df_chart.set_index("Hour"), height=360, use_container_width=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    with st.expander("View Technical Simulation Report"):
        st.json(report)

    st.markdown("""
    <div style="margin-top:2rem; padding-top:1rem; border-top:1px solid var(--wire); text-align:center;">
        <span style="font-family:var(--font-mono); font-size:0.62rem; color:var(--text-lo); letter-spacing:0.06em; font-weight:300; opacity:0.5;">
            Simulation data for planning purposes only — EV Planner Pro
        </span>
    </div>
    """, unsafe_allow_html=True)

elif not st.session_state.chat_started:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⚡ ∿</div>
        <div class="empty-text">
            Select a <em>Quick Action</em> above or type a question
            to begin your infrastructure analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)