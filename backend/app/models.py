from typing import Optional
from pydantic import BaseModel, Field


class AgentARequest(BaseModel):
    subject: str = Field(..., description="High-level subject to explore")
    country: Optional[str] = Field(None, description="Country context (optional)")
    budget: Optional[float] = Field(None, description="Budget available (optional)")


class AgentAResponse(BaseModel):
    subject: str
    country: Optional[str] = None
    budget: Optional[float] = None
    result: str
