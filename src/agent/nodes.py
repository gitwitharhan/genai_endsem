from src.utils.mapping import map_region_to_location
from src.simulation.generate_session import generate_sessions
from src.model.predict import predict_batch
from src.processing.demand_summary import summarize
from src.rag.retriever import get_retriever
from src.agent.llm import build_prompt, call_llm


# ================= DEMAND =================
def analyze_demand(state):

    mapped_location = map_region_to_location(state["region"])

    df = generate_sessions(mapped_location, 200)
    df["predicted_energy"] = predict_batch(df)

    summary = summarize(df)

    return {
        "summary": summary,
        "mapped_location": mapped_location
    }


# ================= LOAD =================
def detect_high_load(state):

    demand = state["summary"]["total_daily_demand"]

    if demand > 1000:
        load = "High"
    elif demand > 500:
        load = "Medium"
    else:
        load = "Low"

    return {"load_level": load}


# ================= RAG =================
def retrieve_guidelines(state):

    retriever = get_retriever()
    docs = retriever.invoke(state["query"])

    # 🔥 FALLBACK CHECK
    if not docs or len(docs) == 0:
        return {"guidelines": "No specific local guidelines found."}

    guidelines = " ".join([d.page_content for d in docs])

    if len(guidelines.strip()) < 20:
        return {"guidelines": "No specific local guidelines found."}

    return {"guidelines": guidelines}


# ================= LLM =================
def plan_infrastructure(state):

    prompt = build_prompt(
        state["query"],
        state["summary"],
        state["guidelines"],
        state.get("history", [])
    )

    response = call_llm(prompt)

    return {"final_response": response}


# ================= REPORT =================
def generate_report(state):

    return {
        "final_report": {
            "location": state["location"],
            "mapped_location": state["mapped_location"],
            "demand_summary": state["summary"],
            "load_level": state["load_level"],
            "response": state["final_response"]
        }
    }