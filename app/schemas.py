from pydantic import BaseModel
from typing import Optional

class TextInput(BaseModel):
    text: str

class FactorOutput(BaseModel):
    factors: list
    confidence: float

class RiskOutput(BaseModel):
    risk_level: str
    score: int
    rationale: list

class FinalOutput(BaseModel):
    risk_level: str
    factors: list
    recommendations: list
    status: str
