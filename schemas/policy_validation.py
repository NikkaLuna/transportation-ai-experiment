from pydantic import BaseModel, Field
from typing import List

class PolicyValidationResult(BaseModel):
    policy_matches: List[str] = Field(default_factory=list)
    compliance_warnings: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0")