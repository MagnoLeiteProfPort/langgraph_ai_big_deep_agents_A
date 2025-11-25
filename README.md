# 🚀 **Agent A Orchestrator — Full-Stack AI Agentic System**

A modern multi-agent system built with **LangChain**, **LangGraph**, **FastAPI**, **Django**, and **React**.  
Agent A dynamically generates exploration axes and units of analysis, then orchestrates multiple downstream calls to **Agent B**, aggregates the results, and returns a synthesized answer.

This project provides:

- 🧠 **Agent A (LangGraph Orchestrator)**
- 🤝 **Integration with Agent B (external FastAPI agent)**
- 🌐 **Frontend (Django + React)**
- ⚡ **Backend (FastAPI)**
- 🎛️ **Optional parameters (COUNTRY, BUDGET)**
- 🛠️ **Clean architecture, ready for extension & production-grade patterns**

---

# 📁 **Project Structure**

```
project/
│
├── backend/
│   ├── app/
│   │   ├── agent.py
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── __init__.py
│   ├── .env
│   ├── requirements.txt
│   └── ...
│
└── frontend/
    ├── agent_frontend/
    ├── core/
    ├── manage.py
    ├── requirements.txt
    └── ...
```

---

# 🌐 **System Architecture Overview**

```
+------------------+        +------------------+        +------------------+
|   Frontend       | -----> |   Agent A API    | -----> |     Agent B      |
| Django + React   | <----- |   FastAPI        | <----- |   FastAPI API    |
+------------------+        +------------------+        +------------------+
            |                          |                          |
            |                          v                          |
            |               LangGraph Orchestrator                 |
            |               create_react_agent()                   |
            |                          |                          |
            |                          v                          |
            |               Tool Calls (call_agent_b)              |
            v                                                     v
    User Input UI                                     Multi-call workflow
```

---

# 🎯 **Core Functionality**

## **1. User enters:**

- **SUBJECT** (required)
- **COUNTRY** (optional)
- **BUDGET** (optional)

## **2. Agent A performs:**

1. Calls an LLM to:
   - derive **Axis of Exploration**
   - derive **N Units of Analysis** (from `.env`)
2. For each unit:
   - Calls **Agent B** via `/run`
3. Collects all Agent B responses
4. Synthesizes a human-readable answer for the frontend

## **3. Frontend displays:**

- 📝 The input form
- 📦 The final result, beautifully formatted

---

# ⚙️ **Backend (Agent A) Setup**

## **1. Navigate into backend**

```bash
cd backend
```

## **2. Create virtual environment**

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
```

## **3. Install dependencies**

```bash
pip install -r requirements.txt
```

## **4. Configure .env**

Create or edit:

```
openai_api_key=YOUR_KEY

# Agent A execution settings
n_units=3
ideal_roles=3
external_research=true
constraints="budget=5000, limited capital, MVP <= 60 days"
complex_unit=false

# Agent B endpoint
agent_b_url=http://127.0.0.1:8000/run
```

## **5. Start Agent A**

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

---

# 🔁 **Agent B Requirements**

Agent B must expose:

```
POST /run
```

Example:

```json
{
  "axis_of_exploration": "AI adoption",
  "unit_of_analysis": "AI usage among SMEs",
  "ideal_roles": 3,
  "external_research": true,
  "constraints": "limited capital, MVP <= 60 days",
  "complex_unit": false,
  "country": "Switzerland"
}
```

---

# 🌐 **Frontend Setup (Django + React)**

## **1. Navigate**

```bash
cd frontend
```

## **2. Virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate
```

## **3. Install**

```bash
pip install -r requirements.txt
```

## **4. Migrate**

```bash
python manage.py migrate
```

## **5. Run**

```bash
python manage.py runserver 8002
```

Open:

👉 **http://127.0.0.1:8002**

---

# 🧠 **Agent Logic (LangGraph)**

Uses:

```python
create_react_agent(
    llm,
    tools=[call_agent_b],
    state_modifier="You are Agent A..."
)
```

---

# 🧪 **Test Agent A**

```bash
curl -X POST http://127.0.0.1:8001/run   -H "Content-Type: application/json"   -d "{"subject":"AI in healthcare"}"
```

---

LOAD THE FULL SET OF COMPONENTS

### BACKEND A

cd "C:\Users\MagnodaSilvaLeite(t2\Documents\Magno_Personal\AI\Portfolio\langgraph_ai_big_deep_agents_A/backend"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

### FRONTEND A

cd "C:\Users\MagnodaSilvaLeite(t2\Documents\Magno_Personal\AI\Portfolio\langgraph_ai_big_deep_agents_A/frontend"
.venv/Scripts/Activate
python manage.py runserver 8002
Quit the server with CTRL-BREAK.

### BACKEND B

cd "C:\Users\MagnodaSilvaLeite(t2\Documents\Magno_Personal\AI\Portfolio\langgraph_ai_big_deep_agents_B"
uvicorn app.api:app --reload

# ⭐ **End of Documentation**
