import os
from typing import Any, Dict, Optional

import httpx
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .config import settings
from .models import AgentARequest

if settings.openai_api_key:
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key


@tool
def call_agent_b(
    axis_of_exploration: str,
    unit_of_analysis: str,
    country: str,
    budget: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Call downstream Agent B (/run) with the given axis, unit, country and optional budget.

    If Agent B times out or returns an HTTP error, this function returns a structured
    error instead of raising, so the orchestrator agent can still summarize what went
    wrong instead of the whole API crashing.
    """
    constraints = settings.constraints

    # If a runtime budget is provided, optionally override "budget=5000"
    if budget is not None and "budget=5000" in constraints:
        constraints = constraints.replace("budget=5000", f"budget={int(budget)}")

    payload = {
        "axis_of_exploration": axis_of_exploration,
        "unit_of_analysis": unit_of_analysis,
        "ideal_roles": settings.ideal_roles,
        "external_research": settings.external_research,
        "constraints": constraints,
        "complex_unit": settings.complex_unit,
        "country": country,
    }

    try:
        # You can tweak timeout here if Agent B does heavy work
        with httpx.Client(timeout=220.0) as client:
            resp = client.post(settings.agent_b_url, json=payload)
            resp.raise_for_status()
            data = resp.json()

        return {
            "ok": True,
            "request": payload,
            "response": data,
        }

    except httpx.ReadTimeout:
        # Agent B did not answer in time
        return {
            "ok": False,
            "request": payload,
            "error_type": "timeout",
            "error_message": f"Timed out contacting Agent B at {settings.agent_b_url}",
        }
    except httpx.HTTPError as e:
        # Any other HTTP-related error (connection refused, 500, etc.)
        status = getattr(getattr(e, "response", None), "status_code", None)
        body = getattr(getattr(e, "response", None), "text", None)
        return {
            "ok": False,
            "request": payload,
            "error_type": "http_error",
            "error_message": f"HTTP error talking to Agent B: {e}",
            "status_code": status,
            "response_body": body,
        }


SYSTEM_PROMPT = f"""
You are Agent A, a LangGraph/LangChain ReAct-style coordinator agent.

Your job:
1. From the user-provided SUBJECT, COUNTRY, and BUDGET:
   - Propose ONE clear, concise "Axis of exploration" (string).
   - Propose exactly N "Units of analysis" related to that axis, where N = {settings.n_units}.
     Each unit should be specific, practical, and business-relevant.

2. For EACH unit of analysis:
   - Call the tool `call_agent_b` with:
       - axis_of_exploration = the axis you defined
       - unit_of_analysis = the specific unit
       - country = user-provided country
       - budget = user-provided budget (use it to adjust constraints if appropriate)

3. After you have called the tool for all units and received all results:
   - Synthesize a final answer that:
       - Clearly explains the axis of exploration.
       - Lists each unit of analysis in a structured way.
       - Summarizes what Agent B returned for each unit (no raw JSON).
       - Connects the insights to the given budget and constraints.
       - Highlights implications for MVP <= 60 days and limited capital.

Environment config you must respect on every call to Agent B:
- ideal_roles = {settings.ideal_roles}
- external_research = {settings.external_research}
- constraints (base) = "{settings.constraints}"
- complex_unit = {settings.complex_unit}
- number_of_units (N) = {settings.n_units}

Output format:
- Use a human-readable structure, for example:

  Axis of Exploration
  -------------------
  [1–2 paragraphs]

  Units of Analysis
  -----------------
  1. [Unit 1 name]
  2. [Unit 2 name]
  3. [Unit 3 name]
  (...)

  Detailed Results per Unit
  -------------------------
  [For each unit, 1–3 short paragraphs summarizing Agent B's output]

  Recommended Next Steps (MVP <= 60 days)
  ---------------------------------------
  [Concrete, actionable suggestions given the budget and timeline]

Do NOT output raw JSON. You are writing for a human stakeholder and product/strategy team.
"""


# Underlying LLM
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
)

# Build the ReAct-style agent using LangGraph's prebuilt helper
agent = create_react_agent(
    model=model,
    tools=[call_agent_b],
    prompt=SYSTEM_PROMPT,
)

def build_agent_user_message(req: AgentARequest) -> str:
    """
    Build the user-facing message that will be passed to the agent.

    SUBJECT is the central idea.
    COUNTRY and BUDGET provide contextual constraints, now Optional.
    """    
    country = req.country or "not specified"
    budget = req.budget if req.budget is not None else "not specified"
    return f"""
SUBJECT: {req.subject}
COUNTRY: {country}
BUDGET: {budget}

Follow the system instructions to:
1) choose an axis of exploration,
2) derive {settings.n_units} units of analysis,
3) call `call_agent_b` for each unit,
4) produce a final synthesized answer.
"""