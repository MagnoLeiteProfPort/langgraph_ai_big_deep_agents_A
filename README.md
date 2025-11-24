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
