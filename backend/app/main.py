from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .agent import agent, build_agent_user_message
from .models import AgentARequest, AgentAResponse

app = FastAPI(title="Agent A API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run", response_model=AgentAResponse)
def run_agent_a(payload: AgentARequest) -> AgentAResponse:
    user_message = build_agent_user_message(payload)
    state = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    final_message = state["messages"][-1]
    content = getattr(final_message, "content", str(final_message))
    return AgentAResponse(subject=payload.subject,
                          country=payload.country,
                          budget=payload.budget,
                          result=content)
