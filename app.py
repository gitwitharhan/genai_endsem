import streamlit as st
import pandas as pd
from src.agent.graph import build_graph

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="⚡ EV Planner Pro",
    page_icon="⚡",
    layout="wide",
)

# ================= PREMIUM CSS =================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c23 100%);
    }
    
    /* Header Styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Chat Bubble Styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    
    /* Card/Metric Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        background: rgba(255, 255, 255, 0.07);
        transform: translateY(-2px);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0c0e12 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Button Animation */
    button {
        transition: transform 0.2s !important;
    }
    button:hover {
        transform: scale(1.02);
    }
    
    </style>
    """, unsafe_allow_html=True)

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "latest_report" not in st.session_state:
    st.session_state.latest_report = None

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("<h1 style='color:#4facfe'>⚡ EV Pro</h1>", unsafe_allow_html=True)
    st.header("🔧 Settings")
    
    location = st.text_input("📍 Location", value="Mumbai", placeholder="e.g. Mumbai")
    region = st.selectbox(
        "🌍 Region Type",
        ["Urban", "Suburban", "Highway"]
    )
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.latest_report = None
        st.rerun()

    st.markdown("""
        <div style='background:rgba(79,172,254,0.1); padding:15px; border-radius:10px; border:1px solid rgba(79,172,254,0.2)'>
        <p style='font-weight:600; margin:0; color:#4facfe'>💡 Expert Tip</p>
        <p style='font-size:0.8rem; opacity:0.8; margin-top:5px'>
        You can ask detailed follow-up questions about infrastructure costs, charger types, or grid stability.
        </p>
        </div>
    """, unsafe_allow_html=True)

# ================= MAIN CONTENT =================
st.markdown("<h1 class='main-header'>⚡ Infrastructure Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='opacity:0.6; margin-top:-10px'>State-of-the-art AI for EV Charging Simulation & Planning</p>", unsafe_allow_html=True)

# ================= SUGGESTIONS =================
suggested_questions = [
    "--- Choose a suggested question ---",
    "⚡ What is the peak demand hour for this area?",
    "🔌 How many chargers are needed to meet the demand?",
    "📊 Show me the full demand pattern analysis.",
    "🏗️ Suggest a long-term infrastructure implementation plan."
]

# React to suggestion selection
selected_suggestion = st.selectbox("💡 Quick Suggestions:", suggested_questions, key="suggestion_box")

# ================= AGENT INVOKER =================
def run_agent(query):
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("🤖 Simulating demand & thinking..."):
        graph = build_graph()
        history = st.session_state.messages[:-1] 

        state = {
            "location": location,
            "region": region,
            "query": query,
            "history": history
        }

        result = graph.invoke(state)
        report = result["final_report"]
        response = report["response"]
        
        st.session_state.latest_report = report

    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Trigger if suggestion selected
if selected_suggestion != suggested_questions[0]:
    query_to_run = selected_suggestion
    # We don't want to rerun immediately here because it might loop
    # Instead, we run the agent and then reset the key if possible, or just let it be.
    # A common trick is to store the last ran query in session state to avoid re-running same suggestion
    if "last_suggestion" not in st.session_state or st.session_state.last_suggestion != query_to_run:
        st.session_state.last_suggestion = query_to_run
        run_agent(query_to_run)
        st.rerun() 

# ================= CHAT HISTORY =================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a custom question..."):
    # If they typed something, we run it
    run_agent(prompt)

# ================= DASHBOARD =================
if st.session_state.latest_report:
    report = st.session_state.latest_report
    summary = report["demand_summary"]
    
    st.divider()
    st.subheader(f"📊 Live Dashboard: {report['location']} ({report['load_level']} Load)")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("⚡ Total Demand", f"{summary['total_daily_demand']} kWh")
    m2.metric("🕒 Peak Hour", f"{summary['peak_hour']}:00")
    m3.metric("🔌 Chargers Needed", summary['chargers_needed'])

    # Dynamic Chart
    if "hourly_profile" in summary:
        hours = list(range(24))
        df_chart = pd.DataFrame({
            "Hour": hours,
            "Demand (kWh)": summary["hourly_profile"]
        })
        st.bar_chart(df_chart.set_index("Hour"))

    with st.expander("🔍 View Technical Simulation Report"):
        st.json(report)