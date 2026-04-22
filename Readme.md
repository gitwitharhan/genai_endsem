# ⚡ Agentic EV Infrastructure Planner

A state-of-the-art, conversational AI platform designed to simulate, analyze, and plan electric vehicle (EV) charging infrastructure. Utilizing agentic workflows and real-time stochastic simulations, this tool provides actionable insights for urban planners and energy providers.

![Tech Stack](https://img.shields.io/badge/Tech-LangGraph%20|%20Groq%20|%20ChromaDB-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Deployed-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)

---

## 🌟 Key Features

### 🤖 Conversational Intelligence

- **Stateful Multi-Turn Chat**: Powered by **LangGraph**, the agent maintains full conversation history, allowing complex follow-up questions.
- **Expert LLM Reasoning**: Integrated with **Groq (Llama 3.1 8B Instant)** for lightning-fast, expert-level infrastructure recommendations.

### 📊 Dynamic Demand Simulations

- **Stochastic Modeling**: Real-time simulation of 200 EV charging sessions using realistic probabilistic distributions (vehicle type, battery capacity, temperature, time of day).
- **Live Dashboards**: Actual ML-predicted hourly demand charts that update dynamically with every query — no hardcoded placeholders.

### 💡 Smart Quick Suggestions

- A **dropdown menu** with 4 curated preset questions for instant analysis.
- **Manual Override**: Users can type any custom question at any time from the chat input.

### 🎨 Premium UI

- **Glassmorphism** chat bubbles and metric card.
- **Gradient header** and **Inter typography** for a professional look.
- **Hover micro-animations** on buttons and metrics for an interactive feel.

---

## 🛠️ Project Architecture

### Agentic Pipeline (LangGraph)

```
User Input
    ↓
1. analyze_demand      → Simulate 200 sessions + ML predict energy
    ↓
2. detect_high_load    → Classify: High / Medium / Low
    ↓
3. retrieve_guidelines → RAG: Fetch top-3 relevant policy chunks
    ↓
4. plan_infrastructure → LLM: Generate conversational recommendation
    ↓
5. generate_report     → Compile structured report for dashboard
    ↓
Final Response + Live Dashboard
```

### Folder Structure

```bash
genai_ENDSEM/
├── app.py                       # Streamlit application (entry point)
├── requirements.txt             # Python dependencies
├── .env                         # Environment secrets (local only, git-ignored)
├── Readme.md                    # This file
├── models/
│   └── ev_demand_model.pkl      # Pre-trained scikit-learn regression model
├── data/
│   └── guidelines.pdf           # EV infrastructure knowledge base (RAG source)
├── chroma_db/                   # ChromaDB vector store (persisted embeddings)
├── docs/                        # Project Documentation
│   ├── project_report.tex       # Full LaTeX project report (research paper style)
│   ├── project_report.docx      # Word (.docx) version (Google Docs compatible)
│   └── generate_report.py       # Script used to generate the .docx report
└── src/                         # Core Source Code
    ├── agent/
    │   ├── graph.py             # LangGraph state machine definition
    │   ├── nodes.py             # Task nodes (demand, RAG, LLM, report)
    │   ├── state.py             # Typed AgentState definition
    │   └── llm.py               # Groq LLM client and prompt builder
    ├── model/
    │   └── predict.py           # Batch prediction logic
    ├── processing/
    │   └── demand_summary.py    # Demand aggregation and hourly profile
    ├── rag/
    │   ├── ingest.py            # PDF ingestion and embedding pipeline
    │   └── retriever.py         # Semantic retrieval from ChromaDB
    ├── simulation/
    │   └── generate_session.py  # Synthetic EV session data generator
    └── utils/
        └── mapping.py           # Region-to-location mapping utility
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.11+
- Groq API Key → [console.groq.com](https://console.groq.com)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/gitwitharhan/genai_endsem.git
cd genai_endsem

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_actual_api_key_here
```

### 4. Run Locally

```bash
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **"Create app"** → **"I have an app"**.
3. Select repository: `gitwitharhan/genai_endsem`, branch: `main`, file: `app.py`.
4. Click **"Advanced settings."** and add your secret:
   ```toml
   GROQ_API_KEY = "your_actual_key_here"
   ```
5. Click **"Deploy!"**.

> ⚠️ **Note:** Set your app's Python version to **3.11** or **3.12** in app settings for best compatibility.

---

## ⚙️ How the Agent Works

| Step | Component                | Action                                                 |
| ---- | ------------------------ | ------------------------------------------------------ |
| 1    | **Simulation**     | Generates 200 stochastic EV sessions based on region   |
| 2    | **ML Model**       | Predicts energy demand for each session (kWh)          |
| 3    | **Summarization**  | Aggregates to total demand, peak hour, chargers needed |
| 4    | **Load Detection** | Classifies area as High / Medium / Low load            |
| 5    | **RAG Retrieval**  | Fetches top-3 relevant policy guidelines from ChromaDB |
| 6    | **LLM Planning**   | Groq Llama 3.1 synthesizes a contextual recommendation |
| 7    | **Report**         | Structured JSON report powers the live dashboard       |

---

## 📚 Documentation

Full project documentation is available in the [`docs/`](./docs/) folder:

| File                                               | Description                                                                          |
| -------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [`project_report.tex`](./docs/project_report.tex)   | LaTeX source — compile with `pdflatex` or upload to [Overleaf](https://overleaf.com) |
| [`project_report.docx`](./docs/project_report.docx) | Word document — open directly in Google Docs or Microsoft Word                      |

The report covers:

- System Architecture & Agentic Pipeline design
- Component-wise technical explanation (Simulation, RAG, LLM, LangGraph)
- Results & qualitative analysis
- Deployment guide and future work

---

## 🧱 Tech Stack

| Layer                 | Technology                               |
| --------------------- | ---------------------------------------- |
| UI Framework          | Streamlit                                |
| Agentic Orchestration | LangGraph                                |
| LLM Inference         | Groq (Llama 3.1 8B Instant)              |
| Vector Store          | ChromaDB                                 |
| Embeddings            | Sentence Transformers (all-MiniLM-L6-v2) |
| ML Prediction         | scikit-learn                             |
| PDF Processing        | LangChain + PyPDF                        |
| Secrets Management    | python-dotenv + Streamlit Secrets        |

---

## 📄 License

This project is licensed under the MIT License.
