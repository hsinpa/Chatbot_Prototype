from typing import Annotated, TypedDict
from pydantic.v1 import BaseModel, Field


class NarratorActionState(TypedDict):
    scenario: Annotated[str, lambda x, y: y]
    narrator_response: str
    is_valid: bool


class ActionType(BaseModel):
    thought: str = Field(..., description='Reason for your validation output')
    is_valid: bool = Field(..., description='Is the action valid')
