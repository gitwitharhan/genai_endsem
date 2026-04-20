# ⚡ Agentic EV Infrastructure Planner

A state-of-the-art, conversational AI platform designed to simulate, analyze, and plan electric vehicle (EV) charging infrastructure. Utilizing agentic workflows and real-time stochastic simulations, this tool provides actionable insights for urban planners and energy providers.

[EV Planner UI Preview](https://img.shields.io/badge/UI-Premium-blueviolet?style=for-the-badge)
[Tech Stack](https://img.shields.io/badge/Tech-LangGraph%20|%20Groq%20|%20ChromaDB-blue?style=for-the-badge)
[[Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://evgptmilestone2.streamlit.app/)

--

## 🌟 Key Features

### 🤖 Conversational Intelligence
- **Stateful Interactions**: Powered by **LangGraph**, the agent maintains full context of the conversation, allowing for complex follow-up questions.
- **Expert Reasoning**: Integrated with **Groq (Llama 3.1)** for lightning-fast, expert-level recommendations on EV infrastructure.

### 📊 Dynamic Demand Simulations
- **Stochastic Modeling**: Real-time generation of EV charging sessions using realistic probabilistic distributions (time, battery capacity, temperature).
- **Interactive Dashboards**: Live metrics and hourly demand charts that update dynamically with every analysis run.

### 💡 Quick Suggestions
- **Smart Prompts**: A dedicated dropdown for quick analysis of peak demand, charger requirements, and long-term planning.
- **Manual Override**: Advanced users can type custom, complex queries for deep-dive investigations.

### 🎨 Premium Aesthetics
- **Modern UI**: A glassmorphic, dark-themed interface with smooth gradients and responsive micro-animations.
- **Professional Analytics**: Clean typography and intuitive layout for clear data interpretation.

--

## 🛠️ Project Architecture & Folder Structure

```bash
genai_ENDSEM/
├── app.py                # Main Streamlit Application (Unified UI & Logic)
├── requirements.txt      # Project Dependencies
├── .env                  # Environment Configuration (API Keys)
├── models/               # Pre-trained ML Models
│   └── ev_demand_model.pkl
├── data/                 # Knowledge Base for RAG
│   └── guidelines.pdf
├── chroma_db/            # Vector Database for RAG Persistence
└── src/                  # Core Source Code
    ├── agent/            # Agentic Core (LangGraph)
    │   ├── graph.py      # State Machine Definition
    │   ├── nodes.py      # Task-specific logic (Demand, RAG, LLM)
    │   ├── state.py      # Typed state management
    │   └── llm.py        # Groq LLM integration & prompting
    ├── model/            # ML Logic
    │   └── predict.py    # Batch prediction logic
    ├── processing/       # Data Analytics
    │   └── demand_summary.py
    ├── rag/              # Retrieval Augmented Generation
    │   ├── retriever.py  # Querying the Vector DB
    │   └── ingest.py     # PDF processing & Embedding creation
    ├── simulation/       # Synthetic Data Generation
    │   └── generate_session.py
    └── utils/            # Shared Helpers (Mapping,etc.)
```

--

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Groq API Key (Get it at [console.groq.com](https://console.groq.com))

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd genai_ENDSEM

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_actual_api_key_here
```

### 4. Running the App
```bash
streamlit run app.py
```

--

## ⚙️ How the Agent Works

1.  **Analyze Demand**: The agent triggers a stochastic simulation of EV charging sessions based on the selected region.
2.  **ML Prediction**: The pre-trained `ev_demand_model` predicts energy requirements for the simulated sessions.
3.  **RAG Enrichment**: Guidelines are retrieved from the local PDF knowledge base (ChromaDB) to ensure results align with regulatory standards.
4.  **Expert Synthesis**: Groq LLM combines conversation history, predicted demand, and retrieved guidelines to generate a conversational report.

--

## 📄 License
This project is licensed under the MIT License.
