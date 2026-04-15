from langgraph.graph import StateGraph, END
from src.agent.state import AgentState

# import nodes
from src.agent.nodes import (
    analyze_demand,
    detect_high_load,
    retrieve_guidelines,
    plan_infrastructure,
    generate_report
)


def build_graph():

    # create graph
    graph = StateGraph(AgentState)

    # ================= ADD NODES =================
    graph.add_node("analyze_demand", analyze_demand)
    graph.add_node("detect_high_load", detect_high_load)
    graph.add_node("retrieve_guidelines", retrieve_guidelines)
    graph.add_node("plan_infrastructure", plan_infrastructure)
    graph.add_node("generate_report", generate_report)

    # ================= ENTRY =================
    graph.set_entry_point("analyze_demand")

    # ================= FLOW =================
    graph.add_edge("analyze_demand", "detect_high_load")
    graph.add_edge("detect_high_load", "retrieve_guidelines")
    graph.add_edge("retrieve_guidelines", "plan_infrastructure")
    graph.add_edge("plan_infrastructure", "generate_report")
    graph.add_edge("generate_report", END)

    # compile graph
    return graph.compile()