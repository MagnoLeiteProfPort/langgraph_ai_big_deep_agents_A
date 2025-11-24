import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def _to_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}

class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    agent_b_url: str = os.getenv("AGENT_B_URL", "http://127.0.0.1:8000/run")
    n_units: int = int(os.getenv("N_UNITS", "3"))
    ideal_roles: int = int(os.getenv("IDEAL_ROLES", "3"))
    external_research: bool = _to_bool(os.getenv("EXTERNAL_RESEARCH", "true"), True)
    constraints: str = os.getenv("CONSTRAINTS", "budget=5000,limited capital, MVP <= 60 days")
    complex_unit: bool = _to_bool(os.getenv("COMPLEX_UNIT", "false"), False)

settings = Settings()
