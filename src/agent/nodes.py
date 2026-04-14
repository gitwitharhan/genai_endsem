def generate_response(state):
    summary = state["summary"]
    guidelines = state["guidelines"]

    return {
        "response": f"""
Demand: {summary['total_daily_demand']} kWh
Peak Hour: {summary['peak_hour']}
Chargers Needed: {summary['chargers_needed']}

Guidelines:
{guidelines}
"""
    }