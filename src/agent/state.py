from typing import TypedDict, Dict, Any, List


class AgentState(TypedDict):
    # ================= USER INPUT =================
    location: str
    region: str
    query: str
    history: List[Dict[str, str]]

    # ================= INTERNAL PROCESS =================
    mapped_location: str
    summary: Dict[str, Any]
    load_level: str
    guidelines: str

    # ================= OUTPUT =================
    final_response: str
    final_report: Dict[str, Any]