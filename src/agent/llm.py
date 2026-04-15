import os
from groq import Groq
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

# Use os.getenv for local dev and st.secrets for Streamlit Cloud
api_key = os.getenv("GROQ_API_KEY") or (st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else None)

client = Groq(api_key=api_key)

def build_prompt(query, summary, guidelines, history):

    history_str = ""
    if history:
        history_str = "\nConversation History:\n" + "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in history])

    return f"""
You are an EV infrastructure expert.
{history_str}

User Question:
{query}

Current Demand Context:
Total Demand: {summary['total_daily_demand']} kWh
Peak Hour: {summary['peak_hour']}
Chargers Needed: {summary['chargers_needed']}

Relevant Guidelines:
{guidelines}

Give a clear, actionable, and conversational EV infrastructure recommendation. If this is a follow-up question, refer to the previous conversation context.
"""

def call_llm(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an EV infrastructure expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content